import pytest
from fastapi.testclient import TestClient
from agno_server.main import app

client = TestClient(app)

def test_root():
    """
    Test the root endpoint for expected status.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Agno MCP server running"}
