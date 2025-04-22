"""
Unit test for Team Lead agent system prompt.
"""
from agno_server.agents.team_lead import TeamLeadAgent, TEAM_LEAD_SYSTEM_PROMPT

def test_team_lead_system_prompt_presence():
    agent = TeamLeadAgent(name="TeamLead")
    assert hasattr(agent, "system_prompt")
    assert TEAM_LEAD_SYSTEM_PROMPT in agent.system_prompt
    assert "Team Lead Agent" in agent.system_prompt
    assert "delegating tasks" in agent.system_prompt  # Accept actual prompt wording
