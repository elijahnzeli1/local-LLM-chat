from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: str

class Conversation(BaseModel):
    id: str = str(uuid.uuid4())
    messages: List[Message]
    created_at: str = datetime.utcnow().isoformat()
    updated_at: str = datetime.utcnow().isoformat()
    title: Optional[str] = None
