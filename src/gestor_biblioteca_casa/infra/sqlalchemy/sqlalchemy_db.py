from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from gestor_biblioteca_casa.infra.sqlalchemy.models import Base

def init_sqla_db(DB_PATH: Path) -> sessionmaker:
    engine = create_engine(f'sqlite:///{DB_PATH}', echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    return SessionLocal

