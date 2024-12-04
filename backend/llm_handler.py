import requests
from typing import Optional

class LMStudioHandler:
    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        max_tokens: int = 800,
        temperature: float = 0.7
    ):
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.temperature = temperature
        
    def generate_response(self, prompt: str) -> Optional[str]:
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/models")
            return response.status_code == 200
        except:
            return False
