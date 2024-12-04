from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from conversation_manager import ConversationManager
from rag_handler import RAGHandler
from auth.analytics_auth import analytics_auth
from analytics.analytics_service import AnalyticsService

router = APIRouter(prefix="/conversation", tags=["conversation"])
conversation_manager = ConversationManager()
rag_handler = RAGHandler()
analytics_service = AnalyticsService()

class ChatMessage(BaseModel):
    message: str
    use_internet: Optional[bool] = False
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[str]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    user_id: str = Depends(analytics_auth.get_current_user)
):
    """Process a chat message and return the response."""
    try:
        # Get or create conversation
        conversation_id = message.conversation_id or conversation_manager.create_conversation()
        
        # Process message
        start_time = datetime.utcnow()
        if message.use_internet:
            response, sources = await rag_handler.process_message_with_web(message.message)
        else:
            response = await conversation_manager.process_message(message.message, conversation_id)
            sources = None
        
        # Calculate response time
        response_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Update analytics
        await analytics_service.update_analytics({
            "user_id": user_id,
            "conversation_id": conversation_id,
            "user_message_length": len(message.message),
            "assistant_message_length": len(response),
            "response_time": response_time,
            "timestamp": datetime.utcnow()
        })
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{conversation_id}")
async def get_conversation_history(
    conversation_id: str,
    user_id: str = Depends(analytics_auth.get_current_user)
):
    """Get the conversation history for a specific conversation."""
    try:
        history = conversation_manager.get_conversation_history(conversation_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/history/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(analytics_auth.get_current_user)
):
    """Delete a specific conversation."""
    try:
        conversation_manager.delete_conversation(conversation_id)
        return {"status": "success", "message": "Conversation deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
