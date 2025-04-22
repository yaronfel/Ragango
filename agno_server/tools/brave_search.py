from .base import SupabaseTool
import httpx
import os

class BraveSearchTool(SupabaseTool):
    name = "BraveSearch"
    description = "Searches the web using Brave Search API. Returns a summary of top results."

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BRAVE_SEARCH_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_SEARCH_API_KEY is required.")

    def run(self, query: str) -> str:
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {"Accept": "application/json", "X-Subscription-Token": self.api_key}
        params = {"q": query, "count": 5}
        resp = httpx.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("web", {}).get("results", []):
            title = item.get("title")
            url = item.get("url")
            snippet = item.get("description")
            results.append(f"- {title}: {url}\n  {snippet}")
        return "\n".join(results) if results else "No results found."

    def execute(self, params: dict) -> str:
        """
        Executes the BraveSearchTool using the query in params.
        Args:
            params (dict): Should contain the key 'query'.
        Returns:
            str: Search results summary.
        """
        query = params.get("query", "")
        return self.run(query)
