from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
import os

api_key = os.getenv("GEMINI_API_KEY")

prd_writer_agent = Agent(
    model=Gemini(id="gemini-pro", api_key=api_key),
    tools=[ReasoningTools()],
    instructions=[
        "Write a detailed product requirements document (PRD) based on the provided structured information.",
        "Be clear, concise, and actionable."
    ],
    description="Expert PRD writer.",
    markdown=True,
)

def write_prd(structured_info: str) -> str:
    """
    Use the Agno PRDWriterAgent to generate a PRD from structured info.
    Args:
        structured_info (str): The structured information for the PRD.
    Returns:
        str: Product requirements document (PRD) text.
    """
    return prd_writer_agent.get_response(structured_info)
