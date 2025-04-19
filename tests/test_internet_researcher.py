"""
Unit test for Internet Researcher agent system prompt.
"""
from agno_server.agents.internet_researcher import InternetResearcherAgent, INTERNET_RESEARCHER_SYSTEM_PROMPT

def test_internet_researcher_system_prompt_presence():
    agent = InternetResearcherAgent(name="InternetResearcher")
    assert hasattr(agent, "system_prompt")
    assert INTERNET_RESEARCHER_SYSTEM_PROMPT in agent.system_prompt
    assert "Internet Researcher Agent" in agent.system_prompt
    assert "WebSearch tool" in agent.system_prompt
    assert "source-attributed summary" in agent.system_prompt
