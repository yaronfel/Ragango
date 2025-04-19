from abc import ABC, abstractmethod
from typing import Any, Dict

class Agent(ABC):
    """
    Abstract base class for all Agno agents.
    Args:
        name (str): Name of the agent.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def act(self, context: Dict[str, Any]) -> Any:
        """
        Perform the agent's primary action based on context.
        Args:
            context (Dict[str, Any]): Shared context for agent decision making.
        Returns:
            Any: Result of the agent's action.
        """
        pass
