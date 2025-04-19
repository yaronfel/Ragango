"""
Unit tests for agno_server.memory (memory management system).
"""
import pytest
from agno_server.memory import MemoryEntry, MemoryStore
from agno_server.communication import AgentRole
from datetime import datetime, timedelta

def test_add_and_get_entry():
    store = MemoryStore()
    entry = MemoryEntry(agent=AgentRole.TEAM_LEAD, type="short_term", data={"foo": "bar"})
    entry_id = store.add_entry(entry)
    fetched = store.get_entry(entry_id)
    assert fetched is not None
    assert fetched.agent == AgentRole.TEAM_LEAD
    assert fetched.data["foo"] == "bar"

def test_query_entries_by_agent_and_type():
    store = MemoryStore()
    e1 = MemoryEntry(agent=AgentRole.TEAM_LEAD, type="short_term", data={})
    e2 = MemoryEntry(agent=AgentRole.PRD_WRITER, type="long_term", data={})
    store.add_entry(e1)
    store.add_entry(e2)
    results = store.query_entries(agent=AgentRole.PRD_WRITER, type="long_term")
    assert len(results) == 1
    assert results[0].agent == AgentRole.PRD_WRITER

def test_query_entries_by_tags():
    store = MemoryStore()
    e1 = MemoryEntry(agent=AgentRole.TEAM_LEAD, type="short_term", data={}, tags=["foo", "bar"])
    e2 = MemoryEntry(agent=AgentRole.PRD_WRITER, type="short_term", data={}, tags=["baz"])
    store.add_entry(e1)
    store.add_entry(e2)
    results = store.query_entries(tags=["bar"])
    assert len(results) == 1
    assert results[0].tags == ["foo", "bar"]

def test_update_entry():
    store = MemoryStore()
    entry = MemoryEntry(agent=AgentRole.TEAM_LEAD, type="short_term", data={"foo": "bar"})
    entry_id = store.add_entry(entry)
    ok = store.update_entry(entry_id, {"foo": "baz"})
    assert ok
    updated = store.get_entry(entry_id)
    assert updated.data["foo"] == "baz"
    assert updated.updated_at > updated.created_at

def test_delete_entry():
    store = MemoryStore()
    entry = MemoryEntry(agent=AgentRole.TEAM_LEAD, type="short_term", data={})
    entry_id = store.add_entry(entry)
    ok = store.delete_entry(entry_id)
    assert ok
    assert store.get_entry(entry_id) is None
