"""
Unit tests for agno_server.communication (agent communication protocol).
"""
import pytest
from agno_server.communication import (
    AgentRole, MessageType, AgentMessage, TurnControl, ErrorMessage,
    AgentCommunicator, ConversationManager
)

def test_agent_message_schema():
    msg = AgentMessage(
        sender=AgentRole.TEAM_LEAD,
        recipient=AgentRole.INTERNET_RESEARCHER,
        type=MessageType.REQUEST,
        content={"query": "Find latest info on X"},
        conversation_id="conv1",
        turn=1
    )
    assert msg.sender == AgentRole.TEAM_LEAD
    assert msg.recipient == AgentRole.INTERNET_RESEARCHER
    assert msg.type == MessageType.REQUEST
    assert msg.content["query"] == "Find latest info on X"
    assert msg.turn == 1

def test_turn_control():
    tc = TurnControl(current_agent=AgentRole.INFO_TAGGER, turn_number=2)
    assert tc.current_agent == AgentRole.INFO_TAGGER
    assert tc.turn_number == 2
    assert tc.finished is False

def test_conversation_manager_turns():
    order = [AgentRole.TEAM_LEAD, AgentRole.INTERNET_RESEARCHER, AgentRole.PRD_WRITER]
    cm = ConversationManager(agent_order=order)
    tc1 = cm.next_turn()
    tc2 = cm.next_turn()
    assert tc1.current_agent == AgentRole.INTERNET_RESEARCHER
    assert tc2.current_agent == AgentRole.PRD_WRITER
    assert tc1.turn_number == 1
    assert tc2.turn_number == 2

def test_error_message_schema():
    err = ErrorMessage(
        sender=AgentRole.PRD_WRITER,
        recipient=AgentRole.ORCHESTRATOR,
        error="Timeout",
        conversation_id="conv2",
        turn=3
    )
    assert err.error == "Timeout"
    assert err.sender == AgentRole.PRD_WRITER
    assert err.recipient == AgentRole.ORCHESTRATOR
    assert err.turn == 3
