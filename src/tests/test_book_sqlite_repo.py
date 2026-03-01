
import pytest
from uuid import uuid4
from datetime import date

from gestor_biblioteca_casa.infra.sqlite.sqlite_book_repo import SQLiteBookRepository
from gestor_biblioteca_casa.infra.sqlite.sqlite_db import create_connection_factory, init_db
from gestor_biblioteca_casa.bootstrap import SQL_PATH, CURRENT_VERSION
from gestor_biblioteca_casa.domain.models import Book

@pytest.fixture
def db_factory(tmp_path):
    return create_connection_factory(tmp_path / 'test_db.db')

@pytest.fixture
def repo(db_factory):
    init_db(db_factory, SQL_PATH, CURRENT_VERSION)
    return SQLiteBookRepository(db_factory)

def test_add_persist_in_sqlite_db_and_list_returns_in_memory_books(repo):
    fake_id1 = uuid4()
    fake_id2 = uuid4()
    fake_id3 = uuid4()

    book1 = Book(id= fake_id1, title='titulo1', author='autor1', acquired_at=date(2026, 1, 10))
    book2 = Book(id= fake_id2, title='titulo2', author='autor2', acquired_at=date(2026, 2, 10))
    book3 = Book(id= fake_id3, title='titulo3', author='autor3', acquired_at=date(2026, 3, 10))

    result1_id = repo.add(book1)
    result2_id = repo.add(book2)
    result3_id = repo.add(book3)

    limit = 10
    offset = 1

    assert result1_id == book1.id

    items = repo.list(limit, offset)
    ids = [b.id for b in items]
    expected_ids = sorted([result1_id, result2_id, result3_id])[offset:limit+offset]

    assert ids == expected_ids