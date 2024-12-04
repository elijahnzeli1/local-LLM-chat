from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.chat_service import generate_chat_response, check_lm_studio_available
from models.chat import Message
from datetime import datetime

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    use_internet: bool = False

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Check LM Studio availability first
        if not await check_lm_studio_available():
            raise HTTPException(
                status_code=503,
                detail="LM Studio is not available. Please make sure it's running on http://localhost:1234"
            )

        # Create message object
        user_message = Message(
            role="user",
            content=request.message,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Generate response
        response_text, conversation_id = await generate_chat_response(
            messages=[user_message],
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_message = str(e)
        if "LM Studio" in error_message:
            raise HTTPException(status_code=503, detail=error_message)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {error_message}"
        )
