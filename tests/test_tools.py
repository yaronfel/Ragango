import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

@pytest.fixture(scope="module")
def test_client():
    with patch("agno_server.main.create_client", return_value=MagicMock()):
        from agno_server.main import app
        return TestClient(app)

# --- ReadRowsTool tests ---
def test_read_rows_success(monkeypatch, test_client):
    class MockResponse:
        data = [{"id": 1, "foo": "bar"}]
    def mock_execute(*args, **kwargs):
        return MockResponse()
    # Patch supabase on app.state
    test_client.app.state.supabase = MagicMock()
    test_client.app.state.supabase.table.return_value.select.return_value.eq.return_value.limit.return_value.execute = mock_execute
    response = test_client.post("/tools/read_rows", json={"table": "test_table"})
    assert response.status_code == 200
    assert "rows" in response.json()

# --- CreateRecordTool tests ---
def test_create_record_success(monkeypatch, test_client):
    class MockResponse:
        data = [{"id": 1, "foo": "bar"}]
    def mock_execute(*args, **kwargs):
        return MockResponse()
    # Patch supabase on app.state
    test_client.app.state.supabase = MagicMock()
    test_client.app.state.supabase.table.return_value.insert.return_value.execute = mock_execute
    response = test_client.post("/tools/create_record", json={"table": "test_table", "records": [{"foo": "bar"}]})
    assert response.status_code == 200
    assert "inserted" in response.json()

# --- UpdateRecordTool tests ---
def test_update_record_success(monkeypatch, test_client):
    class MockResponse:
        data = [{"id": 1, "foo": "baz"}]
    def mock_execute(*args, **kwargs):
        return MockResponse()
    # Patch supabase on app.state
    test_client.app.state.supabase = MagicMock()
    test_client.app.state.supabase.table.return_value.eq.return_value.update.return_value.execute = mock_execute
    response = test_client.post("/tools/update_record", json={"table": "test_table", "filters": {"id": 1}, "values": {"foo": "baz"}})
    assert response.status_code == 200
    assert "updated" in response.json()

# --- DeleteRecordTool tests ---
def test_delete_record_success(monkeypatch, test_client):
    class MockResponse:
        data = []
    def mock_execute(*args, **kwargs):
        return MockResponse()
    # Patch supabase on app.state
    test_client.app.state.supabase = MagicMock()
    test_client.app.state.supabase.table.return_value.eq.return_value.delete.return_value.execute = mock_execute
    response = test_client.post("/tools/delete_record", json={"table": "test_table", "filters": {"id": 1}})
    assert response.status_code == 200
    assert "deleted" in response.json()

# --- Edge and failure cases ---
def test_read_rows_invalid_table(test_client):
    # Simulate an error for nonexistent table
    test_client.app.state.supabase = MagicMock()
    test_client.app.state.supabase.table.side_effect = Exception("Table does not exist")
    response = test_client.post("/tools/read_rows", json={"table": "nonexistent_table"})
    assert response.status_code in (400, 422)

def test_create_record_missing_table(test_client):
    response = test_client.post("/tools/create_record", json={"records": [{"foo": "bar"}]})
    assert response.status_code == 422

def test_update_record_missing_filters(test_client):
    response = test_client.post("/tools/update_record", json={"table": "test_table", "values": {"foo": "baz"}})
    assert response.status_code == 422

def test_delete_record_missing_filters(test_client):
    response = test_client.post("/tools/delete_record", json={"table": "test_table"})
    assert response.status_code == 422
