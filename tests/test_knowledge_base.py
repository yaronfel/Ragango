"""
Unit tests for agno_server.knowledge_base (knowledge base system).
"""
import pytest
from agno_server.knowledge_base import KnowledgeBaseEntry, KnowledgeBase
from datetime import datetime

def test_add_and_get_entry():
    kb = KnowledgeBase()
    entry = KnowledgeBaseEntry(title="Foo", content="Bar content", tags=["foo", "bar"])
    entry_id = kb.add_entry(entry)
    fetched = kb.get_entry(entry_id)
    assert fetched is not None
    assert fetched.title == "Foo"
    assert fetched.content == "Bar content"
    assert "foo" in fetched.tags

def test_query_entries_by_tags():
    kb = KnowledgeBase()
    e1 = KnowledgeBaseEntry(title="A", content="Alpha", tags=["alpha"])
    e2 = KnowledgeBaseEntry(title="B", content="Beta", tags=["beta"])
    kb.add_entry(e1)
    kb.add_entry(e2)
    results = kb.query_entries(tags=["beta"])
    assert len(results) == 1
    assert results[0].title == "B"

def test_query_entries_by_text():
    kb = KnowledgeBase()
    e1 = KnowledgeBaseEntry(title="Doc1", content="The quick brown fox")
    e2 = KnowledgeBaseEntry(title="Doc2", content="Jumps over the lazy dog")
    kb.add_entry(e1)
    kb.add_entry(e2)
    results = kb.query_entries(text="quick")
    assert len(results) == 1
    assert results[0].title == "Doc1"

def test_update_entry():
    kb = KnowledgeBase()
    entry = KnowledgeBaseEntry(title="T", content="Old", tags=["t"])
    entry_id = kb.add_entry(entry)
    ok = kb.update_entry(entry_id, content="New content", metadata={"a": 1})
    assert ok
    updated = kb.get_entry(entry_id)
    assert updated.content == "New content"
    assert updated.metadata["a"] == 1
    assert updated.updated_at > updated.created_at

def test_delete_entry():
    kb = KnowledgeBase()
    entry = KnowledgeBaseEntry(title="T", content="To delete")
    entry_id = kb.add_entry(entry)
    ok = kb.delete_entry(entry_id)
    assert ok
    assert kb.get_entry(entry_id) is None
