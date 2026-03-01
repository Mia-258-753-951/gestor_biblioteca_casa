import sqlite3
from pathlib import Path
from typing import Callable

from gestor_biblioteca_casa.infra.errors import DatabaseInitError


sql_versions = {
    1: '001_initial.sql',
    2: '002_add_acquired_at.sql',
}
ConnectionFactory = Callable[[], sqlite3.Connection] # para typing, definimos el factory
def create_connection_factory(path: Path) -> ConnectionFactory:
    """Crea una factory para obtener conexiones configuradas"""
    def factory() -> sqlite3.Connection:
        conn = sqlite3.connect(str(path))
        conn.row_factory = sqlite3.Row
        # FUTURE ADVISE -> INCLUDE FOREIGN KEYS PRAGMA
        return conn
    return factory

def init_db(factory: ConnectionFactory, SQL_PATH: Path, CURRENT_VERSION: int) -> None:
    """Asegura que la DB existe, tiene el esquema y la versión correcta."""
    # intentamos leer la versión actual
    try:
        with factory() as conn:
            row = conn.execute("SELECT MAX(version) as max_version FROM schema_versions").fetchone()
            current_version = row['max_version'] if row else 0 
    except sqlite3.OperationalError:
    # Si la tabla no existe, asumimos que no existe o está vacía, aplicamos versión 0
        current_version = 0

    # Si versión recibida > CURRENT_VERSION, falla
    if current_version > CURRENT_VERSION:
        raise DatabaseInitError(f'Incompatible version: {current_version}. Current version: {CURRENT_VERSION}.')

    # vamos subiendo una versión hasta que current_version == CURRENT_VERSION
    while current_version < CURRENT_VERSION:
        with (SQL_PATH / sql_versions[current_version + 1]).open('r', encoding='utf-8') as f:
            schema_sql = f.read()
            with factory() as conn:
                conn.executescript(schema_sql)
        current_version += 1
    return     
    
