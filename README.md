# Gestor Biblioteca Casa

Pequeña aplicación en Python para gestionar una biblioteca personal.

El proyecto se está desarrollando como ejercicio de arquitectura limpia, testing y separación de responsabilidades usando:

- **Python**
- **SQLite**
- **SQLAlchemy**
- **Typer (CLI)**
- **FastAPI (API REST)**
- **pytest**
- **ruff**

El objetivo no es solo que funcione, sino practicar **buen diseño de software**.

---

# Características actuales

- Añadir libros
- Listar libros
- Persistencia en base de datos
- CLI funcional con Typer
- API REST con FastAPI
- Backend de persistencia seleccionable
- Tests automatizados

---

# Arquitectura

El proyecto sigue una arquitectura inspirada en **Ports & Adapters / Hexagonal Architecture**.

Separación clara entre:

- **Dominio**
- **Aplicación (servicios)**
- **Infraestructura (repositorios, DB)**
- **Entrypoints (CLI / API)**

Esto permite:

- cambiar backend de persistencia
- testear la lógica sin tocar la infraestructura
- añadir nuevas interfaces (CLI, API, etc.)

---

# Selección de Backend

La aplicación soporta múltiples backends de persistencia:

- `sqlite`
- `sqlalchemy`

El backend se define mediante la variable de entorno:

Ejemplo:

```bash
export BIBLIOTECA_BACKEND=sqlite
o
export BIBLIOTECA_BACKEND=sqlalchemy

# Inicialización del repositorio

La creación del repositorio se hace de forma lazy en bootstrap.py.
Es decir:
* el backend no se decide al importar módulos

* el repositorio no se crea en import-time

Esto evita problemas al:
- importar la CLI
- ejecutar tests
- hacer dependency overrides

El flujo es:

config.get_backend()
        ↓
bootstrap.build_repo()
        ↓
get_book_repo()

get_book_repo() está decorado con:

@lru_cache(maxsize=1)

Esto garantiza que:
- el repositorio se construye una sola vez
- todas las llamadas posteriores reutilizan la misma instancia
- el comportamiento es equivalente a un singleton lazy

# CLI (Typer)

La interfaz CLI se implementa con Typer.

Ejemplo de uso:

uv run python -m gestor_biblioteca_casa.entrypoints.cli.main books new-book "El Quijote" 2026-01-20 --autor Cervantes

Listar libros:

uv run python -m gestor_biblioteca_casa.entrypoints.cli.main books show-books

#Inyección de dependencias en CLI

FastAPI tiene Depends, pero Typer no.
Para evitar que get_repo() se ejecute al importar la CLI, se utiliza un patrón similar mediante:
factory de la app
callback context

La CLI se construye así:

create_app(get_repo)

y los comandos recuperan el repo mediante:

ctx.obj["get_repo"]()

Esto permite:
* evitar repositorios globales

* inyectar repositorios fake en tests

* retrasar la creación del repo hasta ejecutar el comando

# API REST

La API se implementa con FastAPI.

En este caso sí se usa el sistema nativo de dependencias:

Depends(get_repo)

Esto permite hacer overrides fácilmente en tests.

Ejemplo de ejecución:

export BIBLIOTECA_BACKEND=sqlite

uv run uvicorn gestor_biblioteca_casa.entrypoints.api.app:app --reload

# Testing

Los tests usan pytest.

Ejecutar:

uv run pytest

Características:

* uso de tmp_path para bases de datos temporales
* repositorios fake o inyectados
* CLI testada con CliRunner
* aislamiento completo entre tests

Ejemplo de test CLI:

app = create_app(lambda: fake_repo)

result = runner.invoke(
    app,
    ["books", "new-book", "El Quijote", "2026-01-20", "--autor", "Cervantes"]
)

#Estructura del proyecto

gestor_biblioteca_casa/
│
├── config.py
├── bootstrap.py
│
├── domain/
│   └── book.py
│
├── ports/
│   └── book_contract.py
│
├── services/
│   └── book_service.py
│
├── infra/
│   ├── errors.py
│   │
│   ├── sqlite/
│   │   ├── sqlite_book_repo.py
│   │   └── sqlite_db.py
│   │
│   └── sqlalchemy/
│       ├── sqlalchemy_book_repo.py
│       └── sqlalchemy_db.py
│
├── entrypoints/
│   ├── cli/
│   │   ├── main.py
│   │   └── books.py
│   │
│   └── api/
│       └── app.py
│
├── migrations/
│
└── data/

# Herramientas

    * Ruff
    Linting:
        uv run ruff check .

# Objetivos de aprendizaje del proyecto

Este proyecto se utiliza para practicar:

* arquitectura hexagonal
* inyección de dependencias
* testing
* diseño de repositorios
* separación de capas
* uso de FastAPI
* uso de Typer
* SQLAlchemy

Pr# óximos pasos

Posibles mejoras futuras:

autenticación en API

frontend simple

soporte para UTE / empresas en licitaciones (otro proyecto)

paginación más avanzada

filtros de búsqueda

dockerización

logging estructurado

# Nota de diseño

Se ha evitado deliberadamente:
* lógica en import-time
* repositorios globales
* dependencias implícitas

Esto hace que la aplicación sea:

más testeable

más predecible

más fácil de extender