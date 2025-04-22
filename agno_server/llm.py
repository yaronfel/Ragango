import os
import google.generativeai as genai

class GeminiLLM:
    """
    Wrapper for Google Gemini 2.5 Pro API.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def chat(self, prompt: str, system: str = None) -> str:
        """
        Send a prompt to Gemini and return the response.
        Args:
            prompt (str): The user prompt.
            system (str, optional): System instructions/context for the model.
        Returns:
            str: The model's reply.
        """
        # Gemini expects a string, not a list of dicts. Prepend system prompt if provided.
        if system:
            full_prompt = f"{system}\n\n{prompt}"
        else:
            full_prompt = prompt
        response = self.model.generate_content(full_prompt)
        return response.text if hasattr(response, "text") else response['text']
