"""
Unit test for Info Tagger & Structurer agent system prompt.
"""
from agno_server.agents.info_tagger import InfoTaggerAgent, INFO_TAGGER_SYSTEM_PROMPT

def test_info_tagger_system_prompt_presence():
    agent = InfoTaggerAgent(name="InfoTagger")
    assert hasattr(agent, "system_prompt")
    assert INFO_TAGGER_SYSTEM_PROMPT in agent.system_prompt
    assert "Info Tagger & Structurer Agent" in agent.system_prompt
    assert "categorize, and tag" in agent.system_prompt
    assert "structured, tagged summary" in agent.system_prompt
