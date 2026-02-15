# gestor_biblioteca_casa

# 1.-Descripción
Se trata de una herramienta para la gestión de las existencias de libros y música en casa. Permite altas y bajas, préstamos,
consultas por título, género, formato (electrónico, físico).
Al margen de pretender que la herramienta sea totalmente funcional y utilizable, el objetivo principal es didáctico. De este modo, a efectos de aprendizaje se ha llevado a cabo una primera implementación directa (sqlite3) + implementación ORM (SQLAlchemy) para comparar enfoques.
Se desarrolla siguiendo los principios DDD y arquitectura hexágonal, con la intención de poder ampliar la herramienta en el futuro.

# 2.- Stack tecnológico
Tooling :
 * Lenguaje  python 3.13.0
 * Gestor de paquetes: uv
 * API: FastAPI
 * CLI: Typer & Rich
 * Base de Datos: SQLite (SQLAlchemy)

# 3.- Guía de inicio rápido
* Ejecución CLI: uv run ... (a desarrollar)
* Ejecuciuón API: uvicorn ... (a desarrollar)


# 4.- 📂 Estructura del Proyecto

El proyecto sigue un **Src Layout** y principios de **Arquitectura Hexagonal**:

GESTOR_BIBLIOTECA_CASA/
├── src/
│   └── gestor_biblioteca_casa/
│       ├── domain/             # Entidades y reglas de negocio puras
│       ├── entrypoints/        # Adaptadores de entrada (Driving Adapters)
│       │   ├── api/            # Implementación de FastAPI (REST)
│       │   └── cli/            # Implementación de Typer (Consola)
│       ├── infra/              # Adaptadores de salida (Driven Adapters - DB, etc.)
│       ├── ports/              # Interfaces/Protocolos para desacoplamiento
│       ├── services/           # Casos de uso (Application Layer)
│       ├── __init__.py
│       └── __main__.py         # Punto de entrada principal del paquete
├── tests/                      # Pruebas unitarias y de integración
├── .gitignore
├── .python-version
├── pyproject.toml              # Configuración de uv y dependencias
├── README.md
└── uv.lock                     # Archivo de bloqueo de versiones de uv

|

# 5.- Testing y calidad
    * Test: pytest
    * Linting: ruff

# 6.- Documentación de la API
    A desarrollar