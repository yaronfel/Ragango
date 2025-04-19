import pytest
from fastapi.testclient import TestClient
from agno_server.main import app

client = TestClient(app)

# --- ReadRowsTool tests ---
def test_read_rows_success(monkeypatch):
    class MockResponse:
        data = [{"id": 1, "foo": "bar"}]
    def mock_execute(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(app.supabase.table("test_table").select("*"), "execute", mock_execute)
    response = client.post("/tools/read_rows", json={"table": "test_table"})
    assert response.status_code == 200
    assert "rows" in response.json()

# --- CreateRecordTool tests ---
def test_create_record_success(monkeypatch):
    class MockResponse:
        data = [{"id": 1, "foo": "bar"}]
    def mock_execute(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(app.supabase.table("test_table").insert([{"foo": "bar"}]), "execute", mock_execute)
    response = client.post("/tools/create_record", json={"table": "test_table", "records": [{"foo": "bar"}]})
    assert response.status_code == 200
    assert "inserted" in response.json()

# --- UpdateRecordTool tests ---
def test_update_record_success(monkeypatch):
    class MockResponse:
        data = [{"id": 1, "foo": "baz"}]
    def mock_execute(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(app.supabase.table("test_table").eq("id", 1).update({"foo": "baz"}), "execute", mock_execute)
    response = client.post("/tools/update_record", json={"table": "test_table", "filters": {"id": 1}, "values": {"foo": "baz"}})
    assert response.status_code == 200
    assert "updated" in response.json()

# --- DeleteRecordTool tests ---
def test_delete_record_success(monkeypatch):
    class MockResponse:
        data = [{"id": 1, "foo": "baz"}]
    def mock_execute(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(app.supabase.table("test_table").eq("id", 1).delete(), "execute", mock_execute)
    response = client.post("/tools/delete_record", json={"table": "test_table", "filters": {"id": 1}})
    assert response.status_code == 200
    assert "deleted" in response.json()

# --- Edge and failure cases ---
def test_read_rows_invalid_table():
    response = client.post("/tools/read_rows", json={"table": "nonexistent_table"})
    assert response.status_code in (400, 422)

def test_create_record_missing_table():
    response = client.post("/tools/create_record", json={"records": [{"foo": "bar"}]})
    assert response.status_code == 422

def test_update_record_missing_filters():
    response = client.post("/tools/update_record", json={"table": "test_table", "values": {"foo": "baz"}})
    assert response.status_code == 422

def test_delete_record_missing_filters():
    response = client.post("/tools/delete_record", json={"table": "test_table"})
    assert response.status_code == 422
