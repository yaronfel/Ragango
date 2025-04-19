from agno.tools.base import Tool
import httpx
import os

class BraveSearchTool(Tool):
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
