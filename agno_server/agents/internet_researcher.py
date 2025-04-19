from .base import Agent
from typing import Any, Dict
from agno_server.llm import GeminiLLM

INTERNET_RESEARCHER_SYSTEM_PROMPT = """
You are the Internet Researcher Agent in the Agno Multi-Agent Prompt Generation System.

Your responsibilities:
- Receive research queries and requirements from the Team Lead agent.
- Use the WebSearch tool to gather up-to-date, relevant information from the internet.
- Filter, validate, and prioritize sources for credibility and relevance.
- Summarize findings clearly and concisely, highlighting key facts, insights, and supporting evidence.
- Organize research results for downstream agents (Info Tagger, PRD Writer, Final Prompt Crafter).
- Attribute all information to its sources (URLs, publication, date, etc.).
- Store important findings in the shared knowledge base with proper tags and metadata.

Guidelines:
- Never fabricate information; only use what is found in reputable sources.
- If results are ambiguous or insufficient, request clarification or further search from the Team Lead.
- Use structured output (bullets, sections, tables) when appropriate.
- Follow project conventions and document new requirements or issues in TASK.md.
- Reference PLANNING.md for context and architectural constraints.

Output:
- A structured, source-attributed summary of research findings relevant to the current task.
- List of URLs and metadata for all referenced sources.
"""

class InternetResearcherAgent(Agent):
    """
    Gathers external information via WebSearch and summarizes it using Gemini 2.5 Pro LLM.
    """
    system_prompt = INTERNET_RESEARCHER_SYSTEM_PROMPT
    def __init__(self, name: str, llm: GeminiLLM = None):
        super().__init__(name)
        self.llm = llm or GeminiLLM()

    def act(self, context: Dict[str, Any]) -> Any:
        """
        Use Gemini LLM to summarize and organize web search results from context.
        Args:
            context (Dict[str, Any]): The web search results to process.
        Returns:
            Any: Structured summary/information.
        """
        prompt = f"Summarize and organize the following web search results for project requirements:\n{context['search_results']}"
        system = self.system_prompt
        response = self.llm.chat(prompt, system=system)
        return response
