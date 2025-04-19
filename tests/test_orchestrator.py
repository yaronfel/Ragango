import pytest
from agno_server.orchestrator import AgnoOrchestrator

@pytest.fixture
def orchestrator():
    return AgnoOrchestrator()

def test_refine_prompt_basic(monkeypatch, orchestrator):
    # Patch agents to avoid real LLM/API calls
    orchestrator.researcher.act = lambda ctx: "web search summary"
    orchestrator.tagger.act = lambda ctx: "tagged info"
    orchestrator.prd_writer.act = lambda ctx: "PRD text"
    orchestrator.prompt_crafter.act = lambda ctx: "Final production-ready prompt"

    user_idea = "Build a tool for summarizing news articles."
    prompt = orchestrator.refine_prompt(user_idea)
    assert prompt == "Final production-ready prompt"

def test_refine_prompt_integration(monkeypatch, orchestrator):
    # This test can be expanded for integration, but here we just check the workflow runs
    orchestrator.researcher.act = lambda ctx: "research"
    orchestrator.tagger.act = lambda ctx: "tags"
    orchestrator.prd_writer.act = lambda ctx: "prd"
    orchestrator.prompt_crafter.act = lambda ctx: "prompt"
    prompt = orchestrator.refine_prompt("Test idea")
    assert prompt == "prompt"

def test_refine_prompt_empty(monkeypatch, orchestrator):
    orchestrator.researcher.act = lambda ctx: ""
    orchestrator.tagger.act = lambda ctx: ""
    orchestrator.prd_writer.act = lambda ctx: ""
    orchestrator.prompt_crafter.act = lambda ctx: ""
    prompt = orchestrator.refine_prompt("")
    assert prompt == ""
