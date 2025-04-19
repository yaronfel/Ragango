from typing import Any, Dict
from agno_server.agents.team_lead import TeamLeadAgent
from agno_server.agents.internet_researcher import InternetResearcherAgent
from agno_server.agents.info_tagger import InfoTaggerAgent
from agno_server.agents.prd_writer import PRDWriterAgent
from agno_server.agents.final_prompt_crafter import FinalPromptCrafterAgent

class AgnoOrchestrator:
    """
    Orchestrates the multi-agent prompt refinement workflow.
    """
    def __init__(self):
        self.team_lead = TeamLeadAgent("Team Lead")
        self.researcher = InternetResearcherAgent("Internet Researcher")
        self.tagger = InfoTaggerAgent("Info Tagger")
        self.prd_writer = PRDWriterAgent("PRD Writer")
        self.prompt_crafter = FinalPromptCrafterAgent("Final Prompt Crafter")

    def refine_prompt(self, user_idea: str) -> str:
        """
        Runs the full prompt refinement workflow from user idea to final prompt.
        Args:
            user_idea (str): The rough user idea or request.
        Returns:
            str: The final, production-ready prompt.
        """
        # Step 1: Team Lead clarifies and delegates
        context = {"user_idea": user_idea}
        # Step 2: Researcher fetches and summarizes external info
        context["search_results"] = self.researcher.act(context)
        # Step 3: Info Tagger organizes and tags info
        context["raw_data"] = context["search_results"]
        context["structured_info"] = self.tagger.act(context)
        # Step 4: PRD Writer drafts requirements
        context["prd"] = self.prd_writer.act(context)
        # Step 5: Final Prompt Crafter synthesizes everything
        context["agent_outputs"] = f"Research: {context['search_results']}\nTags: {context['structured_info']}"
        final_prompt = self.prompt_crafter.act(context)
        return final_prompt
