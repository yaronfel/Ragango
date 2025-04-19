from agno_server.agents.info_tagger_agno import tag_info
from agno_server.agents.internet_researcher_agno import research
from agno_server.agents.prd_writer_agno import write_prd
from agno_server.agents.final_prompt_crafter_agno import craft_prompt

class AgnoOrchestratorAgno:
    """
    Orchestrates the multi-agent prompt refinement workflow using Agno agents.
    """
    def refine_prompt(self, user_idea: str) -> str:
        """
        Runs the full prompt refinement workflow from user idea to final prompt using Agno agents.
        Args:
            user_idea (str): The rough user idea or request.
        Returns:
            str: The final, production-ready prompt.
        """
        # Step 1: Researcher fetches and summarizes external info
        search_results = research(user_idea)
        # Step 2: Info Tagger organizes and tags info
        structured_info = tag_info(search_results)
        # Step 3: PRD Writer drafts requirements
        prd = write_prd(structured_info)
        # Step 4: Final Prompt Crafter synthesizes everything
        agent_outputs = f"Research: {search_results}\nTags: {structured_info}"
        final_prompt = craft_prompt(prd, agent_outputs)
        return final_prompt
