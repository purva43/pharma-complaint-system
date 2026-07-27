"""
Groq API client for AI model inference.
"""

from groq import Groq
from app.config import settings


class GroqClient:
    """Client for Groq API inference."""
    
    def __init__(self):
        """Initialize Groq client with API key from settings."""
        self.client = Groq(api_key=settings.groq_api_key)
        self.primary_model = "gemma2-9b-it"
        self.fallback_model = "llama-3.3-70b-versatile"
    
    async def chat_completion(
        self,
        messages: list[dict],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        response_format: dict = None
    ) -> dict:
        """
        Send chat completion request to Groq API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name (uses primary model if not specified)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            response_format: Response format specification (e.g., {"type": "json_object"})
            
        Returns:
            dict: Response from Groq API
            
        Raises:
            Exception: If API call fails
        """
        try:
            model = model or self.primary_model
            
            params = {
                "messages": messages,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            if response_format:
                params["response_format"] = response_format
            
            response = self.client.chat.completions.create(**params)
            
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        except Exception as e:
            if model == self.primary_model:
                try:
                    params["model"] = self.fallback_model
                    response = self.client.chat.completions.create(**params)
                    return {
                        "content": response.choices[0].message.content,
                        "model": response.model,
                        "usage": {
                            "prompt_tokens": response.usage.prompt_tokens,
                            "completion_tokens": response.usage.completion_tokens,
                            "total_tokens": response.usage.total_tokens,
                        },
                    }
                except Exception as fallback_error:
                    raise Exception(f"Both primary and fallback models failed: {str(e)}, {str(fallback_error)}")
            raise Exception(f"Groq API call failed: {str(e)}")


groq_client = GroqClient()
