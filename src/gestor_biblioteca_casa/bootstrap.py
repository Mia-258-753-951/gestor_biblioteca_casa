from functools import lru_cache
from pathlib import Path
import sqlite3

from gestor_biblioteca_casa.infra.errors import DatabaseInitError, BackendError
from gestor_biblioteca_casa.infra.sqlite.sqlite_book_repo import SQLiteBookRepository
from gestor_biblioteca_casa.infra.sqlite.sqlite_db import init_db, create_connection_factory
from gestor_biblioteca_casa.infra.sqlalchemy.sqlalchemy_db import init_sqla_db
from gestor_biblioteca_casa.infra.sqlalchemy.sqlalchemy_book_repo import SQLAlchemyBookRepository
from gestor_biblioteca_casa.config import get_backend

SQLITE_DB_PATH = Path(__file__).parents[1].resolve() / 'data/sqlite_data.db'
SQLALCHEMY_DB_PATH = Path(__file__).parents[1].resolve() / 'data/sqlalchemy_data.db'
SQL_PATH = Path(__file__).parent.resolve() / 'migrations'
CURRENT_VERSION = 2

def init_sqlite() -> SQLiteBookRepository:
    # Creamos la factory
    db_factory = create_connection_factory(SQLITE_DB_PATH)
    # Validamos o inicilizamos
    try:
        SQLITE_DB_PATH.parent.mkdir(exist_ok=True, parents=True) 
        init_db(db_factory, SQL_PATH, CURRENT_VERSION)
    except sqlite3.Error as e:
        raise DatabaseInitError(f'Unable to initialize Data Base: {e}.')
    
    return SQLiteBookRepository(connection_factory=db_factory)

def init_sqla() -> SQLAlchemyBookRepository:
    SessionLocal = init_sqla_db(SQLALCHEMY_DB_PATH)
    return SQLAlchemyBookRepository(factory=SessionLocal)

# Creamos el repo en función del backend elegido
def build_book_repo():
    backend = get_backend()
    if backend == 'sqlite':
        return init_sqlite()
    if backend == 'sqlalchemy':
        return init_sqla()
    raise BackendError('Unsupported backend.')


# este es el Singleton que llevará el repo a API y CLI
# utilizando lru_chace devolvemos siempre el mismo repo, no reconstruimos cada llamada
@lru_cache(maxsize=1)
def get_book_repo():    
    return build_book_repo()

def clear_book_repo_cache() -> None:
    get_book_repo.cache_clear()