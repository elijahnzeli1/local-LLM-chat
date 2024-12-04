from fastapi import APIRouter
from typing import List
from models.chat import Conversation

router = APIRouter()

@router.get("/conversations", response_model=List[Conversation])
async def get_conversations():
    """Get all conversations"""
    # For now, return an empty list since we don't have persistence yet
    return []
