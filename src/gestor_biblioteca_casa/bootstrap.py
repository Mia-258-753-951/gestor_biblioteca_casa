from pathlib import Path
import sqlite3

from gestor_biblioteca_casa.infra.errors import DatabaseInitError
from gestor_biblioteca_casa.infra.sqlite.sqlite_book_repo import SQLiteBookRepository
from gestor_biblioteca_casa.infra.sqlite.sqlite_db import init_db, create_connection_factory

DB_PATH = Path(__file__).parents[1].resolve() / 'data/sqlite_data.db'
SQL_PATH = Path(__file__).parent.resolve() / 'migrations'
CURRENT_VERSION = 2

# Creamos la factory
db_factory = create_connection_factory(DB_PATH)

# Validamos o inicilizamos
try:
    DB_PATH.parent.mkdir(exist_ok=True, parents=True) 
    init_db(db_factory, SQL_PATH, CURRENT_VERSION)
except sqlite3.Error as e:
    raise DatabaseInitError(f'Unable to strat Data Base: {e}.')

# Si todo OK, inyectamos la factory en el repo
_repo = SQLiteBookRepository(connection_factory=db_factory)

# este es el Singleton que llevará el repo a API y CLI
def get_book_repo():
    return _repo
