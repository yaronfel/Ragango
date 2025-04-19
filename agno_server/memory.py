"""
memory.py
Memory Management System Specification for Agno Multi-Agent System.

Purpose:
- Provide a shared, structured memory for agents to store, retrieve, update, and delete contextual information during prompt refinement workflows.
- Support both short-term (conversation/session) and long-term (persistent/project) memory.

Requirements:
1. MemoryEntry data model with fields:
   - id: str (unique identifier)
   - agent: AgentRole (who created/owns the entry)
   - type: str ("short_term" | "long_term")
   - data: dict (arbitrary structured content)
   - created_at: datetime
   - updated_at: datetime
   - tags: Optional[List[str]]
   - metadata: Optional[dict]
2. MemoryStore interface with methods:
   - add_entry(entry: MemoryEntry) -> str
   - get_entry(entry_id: str) -> Optional[MemoryEntry]
   - query_entries(agent: Optional[AgentRole], type: Optional[str], tags: Optional[List[str]]) -> List[MemoryEntry]
   - update_entry(entry_id: str, data: dict) -> bool
   - delete_entry(entry_id: str) -> bool
3. Thread-safe, in-memory implementation for MVP (can be swapped for DB later).
4. Pydantic for data validation. Use UTC timestamps.
5. Agents access shared memory via MemoryStore interface.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field
from threading import Lock
from .communication import AgentRole

class MemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    agent: AgentRole
    type: str  # "short_term" or "long_term"
    data: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class MemoryStore:
    """
    Thread-safe in-memory store for MemoryEntry objects.
    """
    def __init__(self):
        self._store: Dict[str, MemoryEntry] = {}
        self._lock = Lock()

    def add_entry(self, entry: MemoryEntry) -> str:
        with self._lock:
            self._store[entry.id] = entry
            return entry.id

    def get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        with self._lock:
            return self._store.get(entry_id)

    def query_entries(self, agent: Optional[AgentRole] = None, type: Optional[str] = None, tags: Optional[List[str]] = None) -> List[MemoryEntry]:
        with self._lock:
            results = list(self._store.values())
            if agent:
                results = [e for e in results if e.agent == agent]
            if type:
                results = [e for e in results if e.type == type]
            if tags:
                results = [e for e in results if e.tags and any(tag in e.tags for tag in tags)]
            return results

    def update_entry(self, entry_id: str, data: Dict[str, Any]) -> bool:
        with self._lock:
            entry = self._store.get(entry_id)
            if not entry:
                return False
            entry.data = data
            entry.updated_at = datetime.utcnow()
            self._store[entry_id] = entry
            return True

    def delete_entry(self, entry_id: str) -> bool:
        with self._lock:
            if entry_id in self._store:
                del self._store[entry_id]
                return True
            return False
