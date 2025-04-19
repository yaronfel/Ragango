"""
Unit test for BraveSearchTool (WebSearch tool interface).
"""
import os
import pytest
from agno_server.tools.brave_search import BraveSearchTool

class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data
    def json(self):
        return self._json
    def raise_for_status(self):
        pass

@pytest.fixture(autouse=True)
def patch_httpx(monkeypatch):
    def dummy_get(url, headers, params, timeout):
        return DummyResponse({
            "web": {
                "results": [
                    {"title": "Test Title", "url": "https://example.com", "description": "Test snippet."}
                ]
            }
        })
    monkeypatch.setattr("httpx.get", dummy_get)


def test_brave_search_tool(monkeypatch):
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY", "dummy-key")
    tool = BraveSearchTool()
    result = tool.run("Agno AI")
    assert "Test Title" in result
    assert "https://example.com" in result
    assert "Test snippet." in result
