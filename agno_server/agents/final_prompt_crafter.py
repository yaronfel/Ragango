from .base import Agent
from typing import Any, Dict
from agno_server.llm import GeminiLLM

FINAL_PROMPT_CRAFTER_SYSTEM_PROMPT = """
You are the Final Prompt Crafter Agent in the Agno Multi-Agent Prompt Generation System.

Your responsibilities:
- Receive the PRD and all relevant outputs from other agents.
- Synthesize a single, production-ready prompt that captures all requirements, context, and constraints.
- Ensure the final prompt is clear, unambiguous, and actionable for its intended use (e.g., LLM input, user-facing system, etc.).
- Integrate all structured data, tags, and source attributions as needed.
- Check for completeness, consistency, and alignment with project goals.
- Flag any unresolved questions, ambiguities, or missing information for Team Lead review.
- Store the final prompt in shared memory and the knowledge base with appropriate tags and metadata.

Guidelines:
- Follow best practices for prompt engineering and the conventions described in PLANNING.md.
- Use clear, concise, and precise language.
- Reference all sources, tags, and agent contributions as appropriate.
- If information is missing or unclear, flag it and request clarification.
- Document any new prompt conventions or templates in TASK.md if introduced.

Output:
- A single, production-ready prompt that fulfills all requirements and is ready for deployment or user delivery.
- List of all referenced tags, sources, and any open questions.
"""

class FinalPromptCrafterAgent(Agent):
    """
    Produces the final, polished prompt artifact using Gemini 2.5 Pro LLM.
    """
    system_prompt = FINAL_PROMPT_CRAFTER_SYSTEM_PROMPT
    def __init__(self, name: str, llm: GeminiLLM = None):
        super().__init__(name)
        self.llm = llm or GeminiLLM()

    def act(self, context: Dict[str, Any]) -> Any:
        """
        Use Gemini LLM to synthesize the final prompt from PRD and agent outputs.
        Args:
            context (Dict[str, Any]): The PRD and related outputs to synthesize.
        Returns:
            Any: Final prompt text.
        """
        prompt = f"Synthesize the following PRD and agent outputs into a single, production-ready prompt:\n{context['prd']}\n\nOther agent outputs:\n{context.get('agent_outputs', '')}"
        system = self.system_prompt
        response = self.llm.chat(prompt, system=system)
        return response
