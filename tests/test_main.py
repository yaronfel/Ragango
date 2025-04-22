import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

@pytest.fixture(scope="module")
def test_client():
    with patch("agno_server.main.create_client", return_value=MagicMock()):
        from agno_server.main import app
    return TestClient(app)

def test_root(test_client):
    """
    Test the root endpoint for expected status.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Agno MCP server running"}
