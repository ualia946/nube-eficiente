# Plan — Lógica de ingesta de datos cloud

## Context

El proyecto necesita poblar las tablas `AmbitoNodo` y `Recurso` con datos reales obtenidos de
las APIs de cada proveedor cloud (empezando por Azure). Hoy existe el ABC `CloudProvider` con
`verify_credentials/list_resources/get_costs`, pero `list_resources` y `get_costs` están como
`NotImplementedError`, y la carpeta `ingestion/` está vacía.

El objetivo es definir **qué métodos** necesitan los providers para extraer la información y
**cómo** esa información llega a la base de datos siguiendo buenas prácticas (separación de
responsabilidades: el provider extrae y normaliza; la ingesta persiste).

**Alcance de esta tanda (v1):** `AmbitoNodo` + `Recurso`. La ingesta de costes
(`RegistroCoste` / `get_costs`) se deja para una fase posterior — `get_costs` permanece como
`NotImplementedError` y NO se añade `azure-mgmt-costmanagement` todavía.

## Decisión de arquitectura

**Ports & Adapters.** El provider NO toca la base de datos. Devuelve DTOs normalizados,
idénticos en forma para cualquier nube. La capa `ingestion/` consume esos DTOs y los persiste.

```
CuentaNube (credenciales JSONB)
   │  factory: proveedor → clase provider
   ▼
AzureProvider.list_scopes()    → [ScopeDTO]    ─┐  (sin BD, datos normalizados)
AzureProvider.list_resources() → [ResourceDTO] ─┘
   │
   ▼  ingestion/ (mapea DTO→ORM, resuelve refs nativas→IDs internos, upsert)
AmbitoNodo  ←  Recurso

(get_costs → RegistroCoste: fase posterior, fuera de v1)
```

## Contrato de providers (DTOs)

Nuevo módulo `app/shared/providers/schemas.py` con dataclasses (sin dependencias nuevas):

- `ScopeDTO(tipo_nodo, proveedor_ref_id, nombre, padre_ref_id: str | None)`
  - Azure: subscription (raíz, `padre_ref_id=None`) → resource_group (`padre_ref_id`= ref de la subscription).
- `ResourceDTO(recurso_ref_id, nombre, tipo, ubicacion, estado, propiedades: dict, ambito_ref_id)`
  - `ambito_ref_id` = `proveedor_ref_id` del resource_group al que pertenece.
  - `estado` normalizado al enum del modelo: `activo|detenido|eliminado`.
- `CostDTO` — diferido a la fase de costes (no se implementa en v1).

## Cambios en el ABC `CloudProvider`
[app/shared/providers/cloud_provider.py](app/shared/providers/cloud_provider.py)

- Añadir `list_scopes() -> list[ScopeDTO]`.
- Tipar `list_resources() -> list[ResourceDTO]`.
- `get_costs()`: se mantiene en el ABC como contrato, pero sin implementar en v1
  (queda `NotImplementedError` en Azure). Su firma definitiva se fijará en la fase de costes.

## Implementación Azure
[app/shared/providers/azure/azure_provider.py](app/shared/providers/azure/azure_provider.py)

- `list_scopes()`: `SubscriptionClient` (subscriptions) + `ResourceManagementClient.resource_groups.list()`.
- `list_resources()`: `ResourceManagementClient.resources.list()`; mapear cada recurso a su resource_group
  (parseando su `id` ARM) y normalizar `estado`.
- Construir clientes Azure de forma perezosa (cacheados) reutilizando `self._credential`.
- `get_costs()`: sin cambios en v1 (sigue `NotImplementedError`).

## Capa de ingesta `app/ingestion/`

- `factory.py` → `crear_provider(cuenta: CuentaNube) -> CloudProvider`: mapea `cuenta.proveedor`
  a la clase concreta (`AzureProvider.from_credentials(cuenta.credenciales)`).
- `mappers.py` → funciones puras `ScopeDTO→AmbitoNodo`, `ResourceDTO→Recurso`, `CostDTO→RegistroCoste`.
- `sincronizador.py` → orquesta por `CuentaNube` dentro de una sesión:
  1. `list_scopes()` → upsert `AmbitoNodo`; dos pasadas para resolver `padre_id` (dict ref_nativa→UUID).
  2. `list_resources()` → upsert `Recurso`; mapear `ambito_ref_id` → `AmbitoNodo.id`.
  - Actualizar `cuenta.estado` (`activa`/`error`) según el resultado.
  - (Costes / `RegistroCoste`: paso 3 futuro, fuera de v1.)

Usa `get_db()`/`SessionLocal` de [app/shared/database/session.py](app/shared/database/session.py).

## Idempotencia (re-ejecutable)

Añadir `UniqueConstraint` en claves naturales + migración Alembic, para upsert con `ON CONFLICT`
(vía `sqlalchemy.dialects.postgresql.insert`):
- `ambito_nodo`: `(id_cuenta_nube, proveedor_ref_id)`
- `recurso`: `(id_ambito_nodo, recurso_ref_id)`
- (`registro_coste`: `(id_recurso, fecha)` — se añadirá con la fase de costes.)

## Dependencias
- Ninguna nueva en v1 (`azure-mgmt-resource` ya cubre scopes y recursos).
- `azure-mgmt-costmanagement` se añadirá en la fase de costes.

## Verificación

- Reutilizar/ampliar [app/scripts/test_azure_conection.py](app/scripts/test_azure_conection.py):
  script manual que construye el provider desde `.env`, llama `list_scopes()`/`list_resources()`
  e imprime los DTOs (sin BD) — valida la capa provider de forma aislada.
- Script de ingesta end-to-end: crea una `CuentaNube` de prueba, ejecuta `sincronizar(cuenta)`,
  y consulta las tablas para verificar filas en `AmbitoNodo`/`Recurso`.
- Re-ejecutar el sync y confirmar que NO se duplican filas (valida idempotencia).
- `cd app && alembic upgrade head` para aplicar la migración de unique constraints.
    