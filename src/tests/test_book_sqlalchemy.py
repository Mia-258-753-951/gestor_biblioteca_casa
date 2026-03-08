import pytest
from uuid import uuid4
from datetime import date

from gestor_biblioteca_casa.infra.sqlalchemy.sqlalchemy_book_repo import SQLAlchemyBookRepository 
from gestor_biblioteca_casa.infra.sqlalchemy.sqlalchemy_db import init_sqla_db
from gestor_biblioteca_casa.domain.models import Book


@pytest.fixture
def repo(tmp_path):
    test_path = tmp_path / 'test_db.db'
    session_factory = init_sqla_db(test_path)
    return SQLAlchemyBookRepository(session_factory)

def test_add_persist_in_sqlalchemy_db_and_list_returns_books(repo):
    fake_id1 = uuid4()
    fake_id2 = uuid4()
    fake_id3 = uuid4()

    book1 = Book(id= fake_id1, title='titulo1', author='autor1', acquired_at=date(2026, 1, 10))
    book2 = Book(id= fake_id2, title='titulo2', author='autor2', acquired_at=date(2026, 2, 10))
    book3 = Book(id= fake_id3, title='titulo3', author='autor3', acquired_at=date(2026, 3, 10))

    result1_id = repo.add(book1)
    result2_id = repo.add(book2)
    result3_id = repo.add(book3)

    limit = 2
    offset = 1

    assert result1_id == book1.id

    items = repo.list(limit, offset)
    ids = [b.id for b in items]
    expected_ids = sorted([result1_id, result2_id, result3_id])[offset:limit+offset]

    assert ids == expected_ids

def test_get_backend_normalizes_case(monkeypatch):
    monkeypatch.setenv("BIBLIOTECA_BACKEND", "SQLALCHEMY")
    from gestor_biblioteca_casa.config import get_backend
    assert get_backend() == "sqlalchemy"

def test_add_persists_across_repo_instances(tmp_path):
    db_path = tmp_path / "test_db.db"

    factory1 = init_sqla_db(db_path)
    repo1 = SQLAlchemyBookRepository(factory=factory1)

    book = Book(id=uuid4(), title="titulo1", author="autor1", acquired_at=date(2026, 1, 10))
    repo1.add(book)

    factory2 = init_sqla_db(db_path)
    repo2 = SQLAlchemyBookRepository(factory=factory2)

    items = repo2.list(limit=10, offset=0)
    assert [b.id for b in items] == [book.id]