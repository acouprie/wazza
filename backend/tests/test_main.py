from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root(test_app):
    response = client.get("/")
    assert response.status_code == 404
