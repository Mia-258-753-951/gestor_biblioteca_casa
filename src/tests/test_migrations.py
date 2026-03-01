from uuid import uuid4
from datetime import date
import pytest

from gestor_biblioteca_casa.infra.sqlite.sqlite_book_repo import SQLiteBookRepository
from gestor_biblioteca_casa.infra.sqlite.sqlite_db import create_connection_factory, init_db
from gestor_biblioteca_casa.bootstrap import SQL_PATH
from gestor_biblioteca_casa.services.book_service import list_books

@pytest.fixture
def db_factory(tmp_path):
    return create_connection_factory(tmp_path / 'test_db.db')

def test_upgrade_v1_to_v2_backfills_acquired_at(db_factory):    
    init_db(db_factory, SQL_PATH, CURRENT_VERSION=1)
    
    with db_factory() as conn:
        conn.execute('''
                     INSERT INTO books (id, title, author)
                     VALUES(?, ?, ?)
                     ''', (uuid4().hex, 'Prueba_schema', 'Autor de prueba')
        )
        conn.commit()
        row_v1 = conn.execute("SELECT * FROM books").fetchone()
        titulo_v1 = row_v1['title']
        autor_v1 = row_v1['author']
        id_v1 = row_v1['id']
        assert 'acquired_at' not in row_v1.keys()
        assert titulo_v1 == 'Prueba_schema'
        assert autor_v1 == 'Autor de prueba'
        assert isinstance(id_v1, str)

    init_db(db_factory, SQL_PATH, CURRENT_VERSION=2)
    repo = SQLiteBookRepository(db_factory)
    
    libro_v2 = list_books(repo, 20, 1)

    assert len(libro_v2) == 1
    assert libro_v2[0].acquired_at == date(2025, 1, 1)
    assert libro_v2[0].id.hex == id_v1

    
  


