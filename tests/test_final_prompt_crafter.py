"""
Unit test for Final Prompt Crafter agent system prompt.
"""
from agno_server.agents.final_prompt_crafter import FinalPromptCrafterAgent, FINAL_PROMPT_CRAFTER_SYSTEM_PROMPT

def test_final_prompt_crafter_system_prompt_presence():
    agent = FinalPromptCrafterAgent(name="FinalPromptCrafter")
    assert hasattr(agent, "system_prompt")
    assert FINAL_PROMPT_CRAFTER_SYSTEM_PROMPT in agent.system_prompt
    assert "Final Prompt Crafter Agent" in agent.system_prompt
    assert "production-ready prompt" in agent.system_prompt
    assert "requirements and is ready for deployment" in agent.system_prompt
