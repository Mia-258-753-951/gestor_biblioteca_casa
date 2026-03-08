import os

from gestor_biblioteca_casa.infra.errors import BackendError

SUPPORTED_BACKENDS = {'sqlite', 'sqlalchemy'}

# hacemos lazy la lectura del backend para no pasarlo antes de timepo en los imports
def get_backend() -> str:
    backend = os.getenv('BIBLIOTECA_BACKEND', 'sqlite').strip().lower() 

    if backend not in SUPPORTED_BACKENDS:
        raise BackendError(
            f"Unsupported backend: {backend!r}."
            f"Supported backends: {', '.join(sorted(SUPPORTED_BACKENDS))}."
        )
    return backend