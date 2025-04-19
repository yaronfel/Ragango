from abc import ABC, abstractmethod
from typing import Any, Dict

class SupabaseTool(ABC):
    """
    Abstract base class for Supabase tools (read, create, update, delete).
    """
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the tool's main action.
        Args:
            params (Dict[str, Any]): Parameters for the tool action.
        Returns:
            Any: Result of the tool operation.
        """
        pass
