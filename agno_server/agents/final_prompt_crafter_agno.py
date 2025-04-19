from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
import os

api_key = os.getenv("GEMINI_API_KEY")

final_prompt_crafter_agent = Agent(
    model=Gemini(id="gemini-pro", api_key=api_key),
    tools=[ReasoningTools()],
    instructions=[
        "Synthesize the PRD and agent outputs into a single, production-ready prompt.",
        "Ensure the final prompt is clear, actionable, and complete."
    ],
    description="Expert prompt crafter for AI systems.",
    markdown=True,
)

def craft_prompt(prd: str, agent_outputs: str = "") -> str:
    """
    Use the Agno FinalPromptCrafterAgent to synthesize the final prompt.
    Args:
        prd (str): The product requirements document.
        agent_outputs (str, optional): Additional agent outputs to include.
    Returns:
        str: Final, production-ready prompt.
    """
    input_text = f"PRD:\n{prd}\n\nOther agent outputs:\n{agent_outputs}"
    return final_prompt_crafter_agent.get_response(input_text)
