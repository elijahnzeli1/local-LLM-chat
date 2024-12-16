from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from conversation_manager import ConversationManager
from conversation.models import ConversationUpdate
from routers.chat import router as chat_router
from routers.conversations import router as conversations_router
from config import get_settings
from rag_handler import RAGHandler

app = FastAPI(title="Local LLM Chat API")
settings = get_settings()
rag_handler = RAGHandler()
conversation_manager = ConversationManager()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")

class MessageRequest(BaseModel):
    message: str
    use_internet: bool = False

class MessageResponse(BaseModel):
    response: str
    conversation_id: str

@app.post("/api/chat/{conversation_id}/message")
async def send_message(conversation_id: str, request: MessageRequest):
    try:
        # Add user message with internet research if enabled
        messages = await conversation_manager.add_message_with_context(
            conversation_id,
            "user",
            request.message,
            request.use_internet
        )
        
        # Format conversation history for LLM
        formatted_history = conversation_manager.format_history_for_llm(conversation_id)
        
        # Get LLM response (implement your LLM integration here)
        # For now, we'll just echo the message
        response = f"Echo: {request.message}"
        
        # Add assistant's response
        conversation_manager.add_message(conversation_id, "assistant", response)
        
        return MessageResponse(
            response=response,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations")
async def get_conversations():
    try:
        return conversation_manager.get_user_conversations("default_user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/conversations")
async def create_conversation(title: Optional[str] = None, mode: str = "normal"):
    try:
        conversation_id = conversation_manager.create_conversation("default_user", title, mode)
        return {"id": conversation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, update: ConversationUpdate):
    try:
        conversation_manager.update_conversation(conversation_id, update)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint to check API status."""
    try:
        # Test LM Studio connection
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.LM_STUDIO_URL}/models")
            lm_studio_available = response.status_code == 200
    except Exception:
        lm_studio_available = False

    return {
        "status": "running",
        "message": "Local LLM Chat API is running",
        "llm_available": rag_handler.is_available(),
        "lm_studio_available": lm_studio_available,
        "lm_studio_url": settings.LM_STUDIO_URL
    }

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    # Ensure required directories exist
    import os
    os.makedirs(settings.CACHE_DIR, exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    # Any cleanup code can go here
    pass
