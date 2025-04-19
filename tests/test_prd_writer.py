"""
Unit test for PRD Writer agent system prompt.
"""
from agno_server.agents.prd_writer import PRDWriterAgent, PRD_WRITER_SYSTEM_PROMPT

def test_prd_writer_system_prompt_presence():
    agent = PRDWriterAgent(name="PRDWriter")
    assert hasattr(agent, "system_prompt")
    assert PRD_WRITER_SYSTEM_PROMPT in agent.system_prompt
    assert "PRD Writer Agent" in agent.system_prompt
    assert "Product Requirements Document" in agent.system_prompt
    assert "well-structured, production-ready PRD" in agent.system_prompt
