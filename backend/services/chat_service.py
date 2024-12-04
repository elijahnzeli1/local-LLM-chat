from typing import List, Optional, Tuple
import httpx
from config import get_settings
from models.chat import Message, Conversation
from datetime import datetime
import uuid
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

settings = get_settings()

async def check_lm_studio_available() -> bool:
    """Check if LM Studio is available"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.LM_STUDIO_URL}/models")
            return response.status_code == 200
    except Exception:
        return False

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry_error_callback=lambda retry_state: (None, None)
)
async def _try_generate_response(client: httpx.AsyncClient, messages: List[Message]) -> dict:
    """Try to generate a response with retries"""
    response = await client.post(
        f"{settings.LM_STUDIO_URL}/chat/completions",
        json={
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ],
            "max_tokens": settings.LM_STUDIO_MAX_TOKENS,
            "temperature": settings.LM_STUDIO_TEMPERATURE,
            "stream": False,
            "model": "llama-3.2-1b-instruct"
        },
        timeout=120.0  # Increase timeout to 120 seconds
    )
    
    if response.status_code != 200:
        error_detail = response.text if response.text else "No error details available"
        raise Exception(f"LM Studio API error (Status {response.status_code}): {error_detail}")
    
    return response.json()

async def generate_chat_response(messages: List[Message], conversation_id: Optional[str] = None) -> Tuple[str, str]:
    """Generate a response using LM Studio API"""
    try:
        # Check if LM Studio is available
        if not await check_lm_studio_available():
            raise Exception("LM Studio is not available. Please make sure it's running on http://localhost:1234")

        # Use a longer timeout for the actual chat completion
        timeout = httpx.Timeout(120.0, connect=5.0)  # Increase total timeout to 120 seconds
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                # Try to generate response with retries
                data = await _try_generate_response(client, messages)
                
                if not data:
                    raise Exception("Failed to generate response after multiple retries")
                
                try:
                    assistant_message = data['choices'][0]['message']['content']
                except (KeyError, IndexError) as e:
                    raise Exception(f"Invalid response format from LM Studio: {str(e)}")
                
                # Generate a new conversation ID if none exists
                if not conversation_id:
                    conversation_id = str(uuid.uuid4())
                    conversation = Conversation(
                        id=conversation_id,
                        messages=messages + [Message(
                            role="assistant",
                            content=assistant_message,
                            timestamp=datetime.utcnow().isoformat()
                        )]
                    )
                    # TODO: Save conversation to database
                
                return assistant_message, conversation_id
                
            except httpx.TimeoutException:
                raise Exception(
                    "Request to LM Studio timed out after 120 seconds. "
                    "The model might be busy or overloaded. Try the following:\n"
                    "1. Restart LM Studio\n"
                    "2. Try a smaller model\n"
                    "3. Reduce the length of your messages"
                )
            except httpx.RequestError as e:
                raise Exception(f"Network error when connecting to LM Studio: {str(e)}")
            
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        raise
