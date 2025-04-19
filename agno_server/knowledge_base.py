"""
knowledge_base.py
Knowledge Base Schema and Access Patterns for Agno Multi-Agent System.

Purpose:
- Provide a persistent, queryable store for structured knowledge used by agents during prompt refinement and research workflows.
- Support semantic and metadata-based querying.

Requirements:
1. KnowledgeBaseEntry data model with fields:
   - id: str (unique identifier)
   - title: str (short summary/label)
   - content: str (main knowledge text)
   - source: Optional[str] (e.g., URL, file, agent)
   - created_at: datetime
   - updated_at: datetime
   - tags: Optional[List[str]]
   - metadata: Optional[dict]
2. KnowledgeBase interface with methods:
   - add_entry(entry: KnowledgeBaseEntry) -> str
   - get_entry(entry_id: str) -> Optional[KnowledgeBaseEntry]
   - query_entries(tags: Optional[List[str]], text: Optional[str], source: Optional[str]) -> List[KnowledgeBaseEntry]
   - update_entry(entry_id: str, content: str, metadata: Optional[dict]) -> bool
   - delete_entry(entry_id: str) -> bool
3. Thread-safe, in-memory implementation for MVP (can be swapped for DB or vector store later).
4. Pydantic for data validation. Use UTC timestamps.
5. Agents access KB via KnowledgeBase interface.
6. Support basic text search (case-insensitive substring match) and tag/source filtering.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field
from threading import Lock

class KnowledgeBaseEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    content: str
    source: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class KnowledgeBase:
    """
    Thread-safe in-memory store for KnowledgeBaseEntry objects.
    """
    def __init__(self):
        self._store: Dict[str, KnowledgeBaseEntry] = {}
        self._lock = Lock()

    def add_entry(self, entry: KnowledgeBaseEntry) -> str:
        with self._lock:
            self._store[entry.id] = entry
            return entry.id

    def get_entry(self, entry_id: str) -> Optional[KnowledgeBaseEntry]:
        with self._lock:
            return self._store.get(entry_id)

    def query_entries(self, tags: Optional[List[str]] = None, text: Optional[str] = None, source: Optional[str] = None) -> List[KnowledgeBaseEntry]:
        with self._lock:
            results = list(self._store.values())
            if tags:
                results = [e for e in results if e.tags and any(tag in e.tags for tag in tags)]
            if text:
                text_lower = text.lower()
                results = [e for e in results if text_lower in e.content.lower() or text_lower in (e.title.lower() if e.title else "")]
            if source:
                results = [e for e in results if e.source == source]
            return results

    def update_entry(self, entry_id: str, content: str, metadata: Optional[dict] = None) -> bool:
        with self._lock:
            entry = self._store.get(entry_id)
            if not entry:
                return False
            entry.content = content
            entry.updated_at = datetime.utcnow()
            if metadata:
                entry.metadata = metadata
            self._store[entry_id] = entry
            return True

    def delete_entry(self, entry_id: str) -> bool:
        with self._lock:
            if entry_id in self._store:
                del self._store[entry_id]
                return True
            return False
