# nube-eficiente — Contexto del proyecto

## Qué es este proyecto

Plataforma SaaS de FinOps para gestión y optimización de costes en la nube. Permite a organizaciones conectar sus cuentas cloud (Azure, AWS, GCP), visualizar recursos, rastrear costes y detectar anomalías mediante IA.

## Estructura del repositorio

```
nube-eficiente/
├── app/                    # Backend Python — única capa Python del proyecto
│   ├── shared/
│   │   ├── database/
│   │   │   ├── models/     # Modelos ORM SQLAlchemy
│   │   │   ├── migrations/ # Migraciones Alembic (antes alembic/ en raíz)
│   │   │   ├── base.py     # DeclarativeBase
│   │   │   └── session.py  # engine + SessionLocal + get_db()
│   │   ├── providers/      # Abstracción de proveedores cloud
│   │   │   ├── cloud_provider.py   # ABC con verify_credentials / list_resources / get_costs
│   │   │   └── azure/
│   │   └── core/           # Utilidades transversales (vacío aún)
│   ├── ingestion/          # Lógica de ingesta de recursos cloud (vacío aún)
│   ├── api/                # API REST backend↔frontend (vacío aún)
│   ├── ai/                 # Modelo de detección de anomalías (vacío aún)
│   ├── scripts/            # Scripts de desarrollo y pruebas manuales
│   ├── alembic.ini         # Configuración de Alembic
│   ├── pyproject.toml      # Empaquetado Python (where = [".."] apunta a raíz)
│   └── requirements.txt    # Dependencias Python
├── frontend/               # React o Astro — no Python, aún vacío
├── infra/                  # IaC — Terraform y scripts de infraestructura
├── docs/
│   └── database/           # Diagrama ER del esquema
├── docker-compose.yml      # PostgreSQL 16 + pgAdmin 4
├── .env                    # Variables de entorno (no commitear)
└── README.md
```

## Base de datos (PostgreSQL + SQLAlchemy 2.0)

### Modelos principales

| Modelo | Tabla | PK | Descripción |
|---|---|---|---|
| `Organizacion` | `organizacion` | UUID | Tenant raíz; plan: free/pro/enterprise |
| `Usuario` | `usuario` | UUID | Pertenece a una organización; rol admin flag |
| `CuentaNube` | `cuenta_nube` | UUID | Credenciales JSONB de proveedor cloud |
| `AmbitoNodo` | `ambito_nodo` | UUID | Árbol jerárquico de scopes (autorreferencial) |
| `Recurso` | `recurso` | Integer | Recurso cloud concreto con propiedades JSONB |
| `RegistroCoste` | `registro_coste` | Integer | Coste diario por recurso (Numeric 16,6) |
| `Anomalia` | `anomalia` | Integer | Anomalía detectada: info/warning/high/critical |
| `Permiso` | `permisos` | (usuario_id, ambito_id) | RBAC: propietario/lector/facturacion |

### Jerarquía de datos

```
Organizacion
└── CuentaNube (azure/aws/gcp)
    └── AmbitoNodo (árbol: subscription → resource_group → ...)
        ├── Recurso
        │   ├── RegistroCoste (serie temporal de costes)
        │   └── Anomalia
        └── Permiso (usuario ↔ ambito)
```

## Comandos frecuentes

```bash
# Levantar base de datos local
docker-compose up -d

# Instalar paquete Python en modo editable
cd app && pip install -e .

# Migraciones — SIEMPRE ejecutar desde app/
cd app && alembic upgrade head
cd app && alembic revision --autogenerate -m "descripcion"
cd app && alembic downgrade -1

# Variables de entorno necesarias
DATABASE_URL=postgresql://cloudwise:cloudwise_dev@localhost:5432/cloudwise
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
AZURE_SUBSCRIPTION_ID=...
```

## Decisiones de diseño

- **Alembic vive en `app/shared/database/migrations/`** — no en la raíz, porque es una herramienta del backend Python, no del monorepo completo.
- **`pyproject.toml` en `app/` con `where = [".."]`** — setuptools busca el paquete `app` un nivel arriba (en la raíz del repo). Instalar con `cd app && pip install -e .`.
- **`frontend/` en la raíz** — React/Astro no es Python; se mantiene separado del paquete Python.
- **`docker-compose.yml` en la raíz** — orquesta todos los servicios (db, pgadmin, y en el futuro backend/frontend).
- **Credenciales en JSONB** — el campo `credenciales` de `CuentaNube` almacena las credenciales del proveedor. Pendiente cifrado en reposo.
- **IDs mixtos** — entidades de negocio principales (organizacion, usuario, cuenta) usan UUID; series temporales (recurso, coste, anomalía) usan Integer autoincremental para eficiencia en inserciones masivas.

## Convenciones

- Idioma del código: **español** para nombres de dominio (modelos, columnas, enums); inglés para infraestructura técnica (métodos de clase, configuración).
- Enums definidos directamente en SQLAlchemy con `name=` para que Alembic los gestione.
- `func.now()` como `server_default` en timestamps; `onupdate=func.now()` en `fecha_actualizacion`.
- `get_db()` es un generador para inyección de dependencias (compatible con FastAPI).

## Estado actual

- [x] Esquema de base de datos completo y migración inicial aplicada
- [x] Abstracción de proveedor cloud (`CloudProvider` ABC) con implementación Azure parcial
- [ ] `ingestion/` — lógica de ingesta de recursos pendiente
- [ ] `api/` — endpoints REST pendientes
- [ ] `ai/` — modelo de detección de anomalías pendiente
- [ ] `frontend/` — interfaz React/Astro pendiente
- [ ] `infra/` — Terraform pendiente
