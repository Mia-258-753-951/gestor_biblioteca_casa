import pytest

from typer.testing import CliRunner

runner = CliRunner()

from gestor_biblioteca_casa.entrypoints.cli.main import create_app
from gestor_biblioteca_casa.infra.sqlite.sqlite_book_repo import SQLiteBookRepository
from gestor_biblioteca_casa.infra.sqlite.sqlite_db import create_connection_factory, init_db
from gestor_biblioteca_casa.bootstrap import SQL_PATH, CURRENT_VERSION


@pytest.fixture
def fake_repo(tmp_path):
    test_path = tmp_path / 'test_db.db'
    factory = create_connection_factory(test_path)
    init_db(factory, SQL_PATH, CURRENT_VERSION)
    return SQLiteBookRepository(factory)

def test_create_new_book_persists_in_memory(fake_repo):
    app = create_app(lambda: fake_repo)

    result = runner.invoke(app, ['books', 'new-book', 'El Quijote', '2026-01-20', '--autor', 'Cervantes'])

    assert result.exit_code == 0
    assert 'Libro guardado con id:' in result.stdout


def test_list_show_stored_book(fake_repo):
    app = create_app(lambda: fake_repo)

    runner.invoke(app, ['books', 'new-book', 'Libro Prueba 1', '2025-02-20', '-a', 'prueba 1'])

    result = runner.invoke(app, ['books', 'show-books'])

    assert 'Libro Prueba 1' in result.stdout
