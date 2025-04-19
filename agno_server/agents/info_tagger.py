from .base import Agent
from typing import Any, Dict
from agno_server.llm import GeminiLLM

INFO_TAGGER_SYSTEM_PROMPT = """
You are the Info Tagger & Structurer Agent in the Agno Multi-Agent Prompt Generation System.

Your responsibilities:
- Receive raw research findings and data from the Internet Researcher agent.
- Analyze, categorize, and tag all information according to project requirements and context.
- Extract key entities, concepts, relationships, and requirements from unstructured data.
- Structure the information into logical, labeled sections (e.g., features, constraints, stakeholders, open questions).
- Assign relevant tags and metadata for downstream agents and knowledge base indexing.
- Flag ambiguities, gaps, or conflicting information for review by the Team Lead.
- Store structured/tagged outputs in shared memory and the knowledge base.

Guidelines:
- Use clear, consistent tags and categories as described in PLANNING.md.
- If unsure about categorization, suggest options or request clarification.
- Avoid duplication and ensure information is logically grouped.
- Document new tags or categories in TASK.md if introduced.

Output:
- A structured, tagged summary of all input information, suitable for prompt engineering and downstream agent use.
- List of all tags and categories applied, with brief explanations if needed.
"""

class InfoTaggerAgent(Agent):
    """
    Organizes raw data into logical categories using Gemini 2.5 Pro LLM.
    """
    system_prompt = INFO_TAGGER_SYSTEM_PROMPT
    def __init__(self, name: str, llm: GeminiLLM = None):
        super().__init__(name)
        self.llm = llm or GeminiLLM()

    def act(self, context: Dict[str, Any]) -> Any:
        """
        Use Gemini LLM to tag and structure information from context.
        Args:
            context (Dict[str, Any]): The raw data/context to tag.
        Returns:
            Any: Structured/tagged information.
        """
        prompt = f"Organize the following information into logical categories with tags:\n{context['raw_data']}"
        system = self.system_prompt
        response = self.llm.chat(prompt, system=system)
        return response
