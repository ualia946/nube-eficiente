# nube-eficiente

Plataforma SaaS de **FinOps** para la gestión y optimización de costes en la nube. Permite a
una organización conectar sus cuentas cloud (Azure, AWS, GCP), visualizar sus recursos,
rastrear costes y detectar anomalías de gasto mediante IA.

## Estado del proyecto

| Componente | Estado |
|---|---|
| Esquema de base de datos + migración inicial | ✅ Completo |
| Abstracción de proveedores cloud (`CloudProvider`) | ✅ Completo |
| Proveedor Azure | ⚠️ Parcial (solo verificación de credenciales) |
| Ingesta de recursos (`ingestion/`) | ❌ Pendiente |
| API REST (`api/`) | ❌ Pendiente |
| Detección de anomalías (`ai/`) | ❌ Pendiente |
| Frontend (`frontend/`) | ❌ Pendiente |
| Infraestructura (`infra/`) | ❌ Pendiente |

Detalle por capa en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#estado-de-implementación).

## Stack tecnológico

- **Backend:** Python 3.12, SQLAlchemy 2.0, Alembic
- **Base de datos:** PostgreSQL 16
- **Cloud:** Azure SDK (`azure-identity`, `azure-mgmt-resource`)
- **Infraestructura local:** Docker Compose (PostgreSQL + pgAdmin)

## Quickstart

Requisitos previos: **Docker** y **Python 3.12+**.

```bash
# 1. Configurar variables de entorno
cp .env.example .env       # Rellenar variables de entorno después. 

# 2. Levantar la base de datos local (PostgreSQL + pgAdmin)
docker-compose up -d

# 3. Instalar el paquete Python en modo editable
cd app && pip install -e .

# 4. Aplicar las migraciones de la base de datos (desde app/)
cd app && alembic upgrade head

# 5. Verificar la conexión con Azure
python app/scripts/test_azure_conection.py
```

pgAdmin queda disponible en [http://localhost:8080](http://localhost:8080)
(`admin@cloudwise.com` / `admin`).

## Estructura del repositorio

```
nube-eficiente/
├── app/          # Backend Python (modelos, proveedores, ingesta, api, ai)
├── frontend/     # React/Astro (pendiente)
├── infra/        # IaC — Terraform (pendiente)
├── docs/         # Documentación
└── docker-compose.yml
```

Árbol completo y explicación de cada capa en
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#estructura-del-monorepo).

## Documentación

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — arquitectura, modelo de datos y
  decisiones de diseño.
- **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** — flujo de ramas, commits, migraciones y
  verificación.
- **[plan-ingesta.md](plan-ingesta.md)** — especificación de la capa de ingesta (próximo
  hito).
