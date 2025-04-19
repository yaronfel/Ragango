from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
import os

# Use GEMINI_API_KEY from environment if set
api_key = os.getenv("GEMINI_API_KEY")

info_tagger_agent = Agent(
    model=Gemini(id="gemini-pro", api_key=api_key),
    tools=[ReasoningTools()],
    instructions=[
        "Organize the provided information into logical categories and tags.",
        "Output only the structured/tagged information, no extra commentary."
    ],
    description="Expert information tagger and structurer.",
    markdown=True,
)

def tag_info(raw_data: str) -> str:
    """
    Use the Agno InfoTaggerAgent to organize and tag information.
    Args:
        raw_data (str): The unstructured information to tag.
    Returns:
        str: Structured/tagged information.
    """
    return info_tagger_agent.get_response(raw_data)
