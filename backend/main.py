from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.chat import router as chat_router
from routers.conversations import router as conversations_router
from config import get_settings
from rag_handler import RAGHandler

app = FastAPI(title="Local LLM Chat API")
settings = get_settings()
rag_handler = RAGHandler()

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
