from fastapi.testclient import TestClient
from api.api import app
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_api_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["Content-Type"] == "application/json"
