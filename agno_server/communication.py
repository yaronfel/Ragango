"""
communication.py
Core agent communication protocol definitions for Agno Multi-Agent System.

Defines message schemas, communication interfaces, and turn-taking logic for agent-to-agent and agent-to-orchestrator interactions.
"""

from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field

class AgentRole(str, Enum):
    TEAM_LEAD = "team_lead"
    INTERNET_RESEARCHER = "internet_researcher"
    INFO_TAGGER = "info_tagger"
    PRD_WRITER = "prd_writer"
    FINAL_PROMPT_CRAFTER = "final_prompt_crafter"
    ORCHESTRATOR = "orchestrator"

class MessageType(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFY = "notify"
    ERROR = "error"

class AgentMessage(BaseModel):
    """
    Standard message format for inter-agent communication.
    """
    sender: AgentRole
    recipient: AgentRole
    type: MessageType
    content: Dict[str, Any]
    conversation_id: str
    turn: int
    metadata: Optional[Dict[str, Any]] = None

class TurnControl(BaseModel):
    """
    Controls which agent has the current turn and manages handoff.
    """
    current_agent: AgentRole
    next_agent: Optional[AgentRole] = None
    turn_number: int
    finished: bool = False

class ErrorMessage(BaseModel):
    """
    Standard error message for protocol violations or failures.
    """
    sender: AgentRole
    recipient: AgentRole
    error: str
    details: Optional[Dict[str, Any]] = None
    conversation_id: str
    turn: int

# Example: Agent communication interface
class AgentCommunicator:
    """
    Handles sending and receiving messages between agents.
    """
    def send_message(self, message: AgentMessage) -> None:
        # Reason: In production, this would enqueue/send the message to the target agent.
        pass

    def receive_message(self) -> AgentMessage:
        # Reason: Would block/wait for incoming message in real system.
        pass

    def handle_error(self, error: ErrorMessage) -> None:
        # Reason: Centralized error handling for agent communication failures.
        pass

# Example: Turn-taking logic
class ConversationManager:
    """
    Manages the conversation flow and agent turn-taking.
    """
    def __init__(self, agent_order: List[AgentRole]):
        self.agent_order = agent_order
        self.turn_number = 0
        self.current_agent_idx = 0

    def next_turn(self) -> TurnControl:
        self.turn_number += 1
        self.current_agent_idx = (self.current_agent_idx + 1) % len(self.agent_order)
        return TurnControl(
            current_agent=self.agent_order[self.current_agent_idx],
            next_agent=self.agent_order[(self.current_agent_idx + 1) % len(self.agent_order)],
            turn_number=self.turn_number,
            finished=False,
        )

    def is_finished(self) -> bool:
        # Reason: Placeholder for logic to determine if conversation is done.
        return False
