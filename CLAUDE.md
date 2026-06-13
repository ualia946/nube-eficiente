# nube-eficiente — Contexto del proyecto

## Qué es

Plataforma SaaS de FinOps para gestión y optimización de costes en la nube. Conecta cuentas
cloud (Azure, AWS, GCP), ingiere recursos, rastrea costes diarios y detecta anomalías de
gasto mediante IA.

> La arquitectura detallada, el modelo de datos completo y las decisiones de diseño viven en
> **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** (fuente única de verdad). El flujo de
> trabajo (ramas, commits, migraciones) está en **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)**.
> Este documento solo recoge lo esencial de alto uso y mis preferencias de trabajo.

## Cómo trabajo en este proyecto (preferencias del usuario)

Sigue estas pautas en cada interacción:

- **Plan-primero.** Ante cambios grandes (una capa nueva, un cambio de esquema, una
  refactorización amplia), presenta primero un plan o spec y **espera mi aprobación** antes
  de implementar. La estructura de referencia es [plan-ingesta.md](plan-ingesta.md).
- **Explica las decisiones.** No entregues solo código: justifica los compromisos y las
  alternativas descartadas, con un nivel didáctico que me ayude a aprender el porqué.
- **Estilo de código y commits.** Español para el dominio (modelos, columnas, enums); inglés
  para infraestructura técnica (métodos, configuración). Commits semánticos con scope:
  `tipo(scope): descripción en minúsculas` (ej. `feat(providers): ...`).
- **Tests y verificación.** Acompaña cada cambio con una forma de verificarlo (un script en
  `app/scripts/` o un test cuando exista la suite) y **propón cómo probarlo** antes de darlo
  por terminado. Aún no hay suite de tests automatizada.
- **Política de documentación.** Regla: cada cosa se documenta donde no se desincroniza.
  Docstrings para lógica de función; `ARCHITECTURE.md` para forma del sistema; `CONTRIBUTING.md`
  para proceso; `README.md` para estado y quickstart. Detalle completo en
  [docs/CONTRIBUTING.md — Política de documentación](docs/CONTRIBUTING.md#política-de-documentación).

## Dónde está cada cosa

| Ruta | Contenido |
|---|---|
| `app/shared/database/models/` | Modelos ORM SQLAlchemy (8 entidades) |
| `app/shared/database/{base,session}.py` | `DeclarativeBase`, engine + `get_db()` |
| `app/shared/database/migrations/` | Migraciones Alembic |
| `app/shared/providers/` | Abstracción multinube: `cloud_provider.py` (ABC), `schemas.py` (DTOs), `azure/` |
| `app/{ingestion,api,ai}/` | Capas pendientes (vacías) |
| `app/scripts/` | Scripts de desarrollo y pruebas manuales |

Estructura completa: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#estructura-del-monorepo).

### Modelos de datos

Para columnas y relaciones exactas **revisa siempre [app/shared/database/models/](app/shared/database/models/)**.

| Modelo | Tabla | PK | Descripción |
|---|---|---|---|
| `Organizacion` | `organizacion` | UUID | Tenant raíz; plan: free/pro/enterprise |
| `Usuario` | `usuario` | UUID | Pertenece a una organización; flag `es_admin` |
| `CuentaNube` | `cuenta_nube` | UUID | Credenciales JSONB de proveedor cloud |
| `AmbitoNodo` | `ambito_nodo` | UUID | Árbol jerárquico de scopes (autorreferencial) |
| `Recurso` | `recurso` | Integer | Recurso cloud concreto con propiedades JSONB |
| `RegistroCoste` | `registro_coste` | Integer | Coste diario por recurso (Numeric 16,6) |
| `Anomalia` | `anomalia` | Integer | Anomalía detectada: info/warning/high/critical |
| `Permiso` | `permisos` | (usuario_id, ambito_id) | RBAC: propietario/lector/facturacion |

Jerarquía: `Organizacion → CuentaNube → AmbitoNodo (árbol) → Recurso → {RegistroCoste, Anomalia}` + `Permiso (usuario ↔ ambito)`.

## Comandos frecuentes

```bash
# Levantar base de datos local (PostgreSQL + pgAdmin)
docker-compose up -d

# Instalar paquete Python en modo editable
cd app && pip install -e .

# Migraciones — SIEMPRE desde app/
cd app && alembic upgrade head
cd app && alembic revision --autogenerate -m "descripcion"
cd app && alembic downgrade -1

# Verificar conexión con Azure
python app/scripts/test_azure_conection.py
```

Variables de entorno: copia `.env.example` a `.env` y rellénalas (`DATABASE_URL` y las
`AZURE_*`). `.env` está en `.gitignore`.

## Convenciones técnicas

- Enums definidos en SQLAlchemy con `name=` para que Alembic los gestione como tipos nativos.
- `func.now()` como `server_default` en timestamps; `onupdate=func.now()` en `fecha_actualizacion`.
- `get_db()` es un generador para inyección de dependencias (compatible con FastAPI).
- Los proveedores devuelven DTOs (`ScopeDTO`/`ResourceDTO`), nunca modelos ORM; la traducción
  DTO → ORM es responsabilidad exclusiva de la capa de ingesta.

## Estado actual

- [x] Esquema de base de datos completo y migración inicial aplicada
- [x] Abstracción de proveedor cloud (`CloudProvider` ABC) + DTOs
- [~] `AzureProvider` — solo `verify_credentials()` implementado
- [ ] `ingestion/` — ingesta de recursos (especificada en [plan-ingesta.md](plan-ingesta.md))
- [ ] `api/` — endpoints REST (requiere añadir FastAPI)
- [ ] `ai/` — modelo de detección de anomalías
- [ ] `frontend/` — interfaz React/Astro
- [ ] `infra/` — Terraform
- [ ] Suite de tests automatizada
