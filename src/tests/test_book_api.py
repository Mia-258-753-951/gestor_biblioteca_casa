
from fastapi.testclient import TestClient
import pytest

from gestor_biblioteca_casa.entrypoints.api.main import app
from gestor_biblioteca_casa.bootstrap import get_book_repo, SQL_SCRIPT, CURRENT_VERSION
from gestor_biblioteca_casa.infra.sqlite.sqlite_db import create_connection_factory, init_db
from gestor_biblioteca_casa.infra.sqlite.sqlite_book_repo import SQLiteBookRepository

# creamos el factory apuntando al path temporal
@pytest.fixture
def db_factory(tmp_path):
    return create_connection_factory(tmp_path / 'test_db.db')

# creamos schema en path temporal y devolvemos repo con factory inyectado
@pytest.fixture
def test_repo(db_factory):
    init_db(db_factory, SQL_SCRIPT, CURRENT_VERSION)    
    return SQLiteBookRepository(db_factory)

# creamos override y cliente que lo aplica, limpiando al salir
@pytest.fixture
def client(test_repo):
    """configura el override y lo limpia después"""
    # esta es la función que sustitye al original
    def override_get_book_repo():
        return test_repo

    app.dependency_overrides[get_book_repo] = override_get_book_repo

    # creamos el cliente dentro del contexto del override
    with TestClient(app) as c:
        yield c
    
    # limpiamos el override al salir
    app.dependency_overrides.clear()

def test_api_creates_then_list(client):
    
    r = client.post('/books/', params={'title': 'prueba1','author': 'author1'})

    data = r.json()

    assert r.status_code == 200
    assert isinstance(data['id'], str)    

    r = client.get('/books/')

    items = r.json()

    assert r.status_code == 200
    assert len(items) == 1
    assert isinstance(items[0]['id'], str)
    assert items[0]['title'] == 'prueba1'
    assert items[0]['author'] == 'author1'

