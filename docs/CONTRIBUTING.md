# Guía de contribución — nube-eficiente

Cómo trabajar en el proyecto: entorno, flujo de ramas, commits, migraciones, verificación y
política de documentación.
Para entender la arquitectura antes de tocar código, lee [ARCHITECTURE.md](ARCHITECTURE.md).

## Índice

- [Entorno de desarrollo](#entorno-de-desarrollo)
- [Flujo de ramas](#flujo-de-ramas)
- [Convención de commits](#convención-de-commits)
- [Migraciones de base de datos](#migraciones-de-base-de-datos)
- [Verificación de cambios](#verificación-de-cambios)
- [Patrón plan-primero para features grandes](#patrón-plan-primero-para-features-grandes)
- [Política de documentación](#política-de-documentación)

---

## Entorno de desarrollo

El [quickstart del README](../README.md#quickstart) cubre la puesta en marcha básica. Notas
adicionales para desarrollo:

- **Python 3.12+** es obligatorio (`requires-python = ">=3.12"`).
- Usa un entorno virtual (`.venv/`, ya ignorado por git):
  ```bash
  python -m venv .venv && source .venv/bin/activate
  cd app && pip install -e .
  ```
- La base de datos local se levanta con Docker. pgAdmin queda en
  [http://localhost:8080](http://localhost:8080) (usuario `admin@cloudwise.com` / `admin`),
  útil para inspeccionar tablas y depurar el esquema.
- Las variables de entorno se cargan desde `.env` (vía `python-dotenv` en
  [app/shared/database/session.py](../app/shared/database/session.py)). Nunca commitees
  `.env`; parte siempre de `.env.example`.

---

## Flujo de ramas

Ramas con prefijo de tipo, descripción en kebab-case:

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feat/` | Nueva funcionalidad | `feat/project-foundation` |
| `refactor/` | Reestructuración sin cambio funcional | `refactor/provider-layer` |
| `docs/` | Solo documentación | `docs/architecture` |
| `fix/` | Corrección de errores | `fix/azure-auth-timeout` |

Las ramas se integran a `main` mediante Pull Request.

---

## Convención de commits

**Commits semánticos** con scope opcional: `tipo(scope): descripción en minúsculas`.

Ejemplos reales del historial del proyecto:

```
feat(providers): add cloud provider interface and Azure implementation
refactor(structure): reorganize project layout for polyglot monorepo
feat(foundation): initialize project structure and database schema
docs(readme): añadir documentación inicial
```

Tipos habituales: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.

---

## Migraciones de base de datos

El proyecto usa **Alembic**, ubicado en `app/shared/database/migrations/`. **Todos los
comandos se ejecutan desde `app/`** (es donde vive `alembic.ini`):

```bash
# Aplicar todas las migraciones pendientes
cd app && alembic upgrade head

# Generar una migración nueva a partir de cambios en los modelos
cd app && alembic revision --autogenerate -m "descripcion del cambio"

# Revertir la última migración
cd app && alembic downgrade -1
```

Tras editar cualquier modelo en [app/shared/database/models/](../app/shared/database/models/),
genera una migración con `--autogenerate` y **revísala manualmente** antes de aplicarla:
Alembic no siempre detecta cambios de enums o de tipos correctamente.

---

## Verificación de cambios

> ⚠️ Aún **no existe una suite de tests automatizada**. Añadir `pytest` está pendiente
> (ver [estado de implementación](ARCHITECTURE.md#estado-de-implementación)).

Mientras tanto, la verificación es manual mediante scripts en `app/scripts/`:

```bash
# Comprobar conexión y credenciales de Azure
python app/scripts/test_azure_conection.py
```

Al implementar una funcionalidad, **acompáñala siempre de una forma de verificarla** (un
script en `app/scripts/`, o un test cuando exista la suite) antes de darla por terminada.

---

## Patrón plan-primero para features grandes

Para funcionalidades de cierto tamaño (una capa nueva, un cambio de esquema, etc.), **antes
de implementar** se redacta una especificación en un archivo Markdown a nivel de raíz, con:
contexto/problema, decisión arquitectónica, contratos/DTOs, cambios por archivo,
consideraciones de idempotencia y plan de verificación.

El ejemplo de referencia es [plan-ingesta.md](../plan-ingesta.md) (spec de la capa de
ingesta). Usa esa estructura como plantilla.

---

## Política de documentación

**Regla raíz:** cada cosa se documenta en el nivel donde no se desincroniza con el código.

### Pregunta de decisión

> ¿Esto lo necesita alguien para entender el **sistema**, o solo para entender **esta función**?

- Si es solo esta función/clase → **docstring o comentario en el propio código**.
- Si es el sistema → **`docs/ARCHITECTURE.md`**.

### Tabla de referencia

| Tipo de cambio | Dónde documentarlo |
|---|---|
| Por qué funciona así una función o clase concreta | Docstring en el código (junto al código) |
| Nueva entidad de dominio, nueva capa, decisión de diseño, cambio de jerarquía | `docs/ARCHITECTURE.md` |
| Nuevo comando, convención, flujo de ramas, cómo migrar, cómo testear | `docs/CONTRIBUTING.md` (este archivo) |
| Cambia el stack, el quickstart o el estado del proyecto | `README.md` + checklist de estado |
| Capa que pasa de pendiente a implementada; preferencia de trabajo nueva | `CLAUDE.md` (checklist + preferencias) |
| Feature grande antes de implementarla | `plan-X.md` en raíz; al terminar, lo durable migra a `ARCHITECTURE.md` |

### Lo que NO va en `ARCHITECTURE.md`

No incluyas detalle de nivel de función (ej. *"el método X recibe estos 3 argumentos"*) — eso
se desincroniza en cuanto cambias el código y es responsabilidad del docstring. `ARCHITECTURE.md`
documenta la **forma** del sistema (capas, relaciones entre módulos, decisiones), no la
**implementación** de cada función.

### Cuándo crece `ARCHITECTURE.md` en archivos separados

Mientras el proyecto sea pequeño, un único `ARCHITECTURE.md` es suficiente y más fácil de
mantener. Si en el futuro el archivo supera las ~500 líneas y necesitas leer solo una parte
habitualmente, pártelo por dominio:

```
docs/
├── ARCHITECTURE.md      # visión general + capas + índice con enlaces
├── data-model.md        # solo el modelo de datos
├── providers.md         # solo la abstracción cloud
└── ingestion.md         # solo la capa de ingesta
```

El índice en `ARCHITECTURE.md` actúa como mapa; cada archivo de dominio se lee solo cuando
necesitas esa parte. **No lo hagas antes de que sea necesario.**
