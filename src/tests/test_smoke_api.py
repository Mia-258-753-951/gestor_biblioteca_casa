from fastapi.testclient import TestClient

from gestor_biblioteca_casa.entrypoints.api.main import app

def test_api_health():
    client = TestClient(app)
    r = client.get('/health')

    assert r.status_code == 200