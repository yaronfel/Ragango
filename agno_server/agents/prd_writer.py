from .base import Agent
from typing import Any, Dict
from agno_server.llm import GeminiLLM

PRD_WRITER_SYSTEM_PROMPT = """
You are the PRD Writer Agent in the Agno Multi-Agent Prompt Generation System.

Your responsibilities:
- Receive structured, tagged information from the Info Tagger & Structurer agent.
- Draft a comprehensive, clear, and actionable Product Requirements Document (PRD) based on the provided information.
- Ensure all requirements, features, constraints, stakeholders, and open questions are accurately captured.
- Organize the PRD using logical sections (e.g., Overview, Goals, Features, User Stories, Constraints, Acceptance Criteria).
- Maintain traceability between requirements and their sources/tags.
- Highlight any ambiguities, gaps, or dependencies for Team Lead review.
- Store the PRD in shared memory and knowledge base with appropriate tags and metadata.

Guidelines:
- Follow best practices for PRD writing and the format described in PLANNING.md.
- Use clear, concise, and unambiguous language.
- If information is missing or unclear, flag it and request clarification.
- Reference all sources and tags where relevant.
- Document any new PRD sections or conventions in TASK.md if introduced.

Output:
- A well-structured, production-ready PRD, suitable for use by the Final Prompt Crafter agent or for direct user review.
- List of all referenced tags, sources, and open questions.
"""

class PRDWriterAgent(Agent):
    """
    Transforms structured information into product requirements using Gemini 2.5 Pro LLM.
    """
    system_prompt = PRD_WRITER_SYSTEM_PROMPT
    def __init__(self, name: str, llm: GeminiLLM = None):
        super().__init__(name)
        self.llm = llm or GeminiLLM()

    def act(self, context: Dict[str, Any]) -> Any:
        """
        Use Gemini LLM to write a product requirements document from context.
        Args:
            context (Dict[str, Any]): The structured information to convert to PRD.
        Returns:
            Any: Product requirements document (PRD) text.
        """
        prompt = f"Write a detailed product requirements document (PRD) based on the following structured information:\n{context['structured_info']}"
        system = self.system_prompt
        response = self.llm.chat(prompt, system=system)
        return response
