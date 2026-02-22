import sqlite3
from pathlib import Path
from typing import Callable


ConnectionFactory = Callable[[], sqlite3.Connection] # para typing, definimos el factory
def create_connection_factory(path: Path) -> ConnectionFactory:
    """Crea una factory para obtener conexiones configuradas"""
    def factory() -> sqlite3.Connection:
        conn = sqlite3.connect(str(path))
        conn.row_factory = sqlite3.Row
        # FUTURE ADVISE -> INCLUDE FOREIGN KEYS PRAGMA
        return conn
    return factory

def init_db(factory: ConnectionFactory, sql_path: Path, expected_version: int) -> None:
    """Asegura que la DB existe, tiene el esquema y la versión correcta."""
    # 1.- intentamos leer la verisón actual
    try:
        with factory() as conn:
            row = conn.execute("SELECT version FROM schema_versions").fetchone()
            current_version = row['version'] if row else None
    except sqlite3.OperationalError:
    # Si la tabla no existe, asumimos que no existe o está vacía
        current_version = None

    # 2.- Si no hay verisón, inicializamos schema (ejecutamos SQL)
    if current_version is None:
        with sql_path.open('r', encoding='utf-8') as f:
            schema_sql = f.read()
            with factory() as conn:
                conn.executescript(schema_sql)
        return     
    
    # 3.- Si hay versión pero no coincide, lanzamos error
    if current_version != expected_version:
        raise sqlite3.Error(
            f'Incompatible version: {current_version}. Expected_version: {expected_version}.'
        )