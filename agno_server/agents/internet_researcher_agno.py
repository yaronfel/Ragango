from agno.agent import Agent
from agno.models.google import Gemini
from agno_server.tools.brave_search import BraveSearchTool
import os

api_key = os.getenv("GEMINI_API_KEY")

internet_researcher_agent = Agent(
    model=Gemini(id="gemini-pro", api_key=api_key),
    tools=[BraveSearchTool()],
    instructions=[
        "Summarize and organize web search results for project requirements.",
        "Always include sources in your summary.",
        "Be concise and focus on actionable insights."
    ],
    description="Expert AI researcher using Brave Search.",
    markdown=True,
)

def research(search_query: str) -> str:
    """
    Use the Agno InternetResearcherAgent to search and summarize information with Brave Search.
    Args:
        search_query (str): The query to search for.
    Returns:
        str: Structured summary with sources.
    """
    return internet_researcher_agent.get_response(search_query)
