"""Ollama API client with streaming support."""

from typing import Iterator, List, Dict
import requests
import json


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize the Ollama client."""
        self.base_url = base_url.rstrip("/")
    
    def chat(self, model: str, messages: List[Dict[str, str]]) -> Iterator[str]:
        """
        Send a chat request and stream the response.
        
        Args:
            model: The model name to use
            messages: List of message dicts with 'role' and 'content'
        
        Yields:
            Response chunks as they arrive
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }
        
        try:
            response = requests.post(url, json=payload, stream=True, timeout=120)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
                    
                    if data.get("done", False):
                        break
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Could not connect to Ollama. Is it running?")
        except requests.exceptions.Timeout:
            raise TimeoutError("Request to Ollama timed out")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")
    
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
