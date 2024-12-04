from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Tag(BaseModel):
    id: str
    name: str
    color: str
    created_at: datetime
    user_id: str

class Category(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    user_id: str

class ConversationMetadata(BaseModel):
    category_id: Optional[str] = None
    tags: List[str] = []
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: str
    is_shared: bool = False
    shared_with: List[str] = []
    last_accessed: datetime
    created_at: datetime

class ConversationUpdate(BaseModel):
    category_id: Optional[str] = None
    tags: Optional[List[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_shared: Optional[bool] = None
    shared_with: Optional[List[str]] = None
