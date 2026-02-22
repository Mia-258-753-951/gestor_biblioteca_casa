
from fastapi.testclient import TestClient
from gestor_biblioteca_casa.entrypoints.api.main import app

client = TestClient(app)

def test_api_creates_then_list():
    
    r = client.post('/books/', params={'title': 'prueba1','author': 'author1'})

    data = r.json()

    assert isinstance(data['id'], str)
    

    r = client.get('/books/')

    items = r.json()

    assert len(items) == 1
    assert isinstance(items[0]['id'], str)
    assert items[0]['title'] == 'prueba1'
    assert items[0]['author'] == 'author1'

