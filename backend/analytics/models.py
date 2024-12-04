from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class MessageStats(BaseModel):
    total_messages: int
    user_messages: int
    assistant_messages: int
    avg_user_length: float
    avg_assistant_length: float
    
class TimeStats(BaseModel):
    hour_distribution: Dict[int, int]  # Hour (0-23) -> message count
    day_distribution: Dict[int, int]   # Day of week (0-6) -> message count
    avg_response_time: float           # Average time between user and assistant messages
    
class CategoryStats(BaseModel):
    category_distribution: Dict[str, int]  # Category name -> conversation count
    most_used_category: Optional[str]
    
class TagStats(BaseModel):
    tag_distribution: Dict[str, int]  # Tag name -> usage count
    most_used_tags: List[str]         # Top tags
    
class ConversationStats(BaseModel):
    total_conversations: int
    active_conversations: int
    avg_messages_per_conversation: float
    avg_conversation_length: float  # In minutes
    
class UserAnalytics(BaseModel):
    user_id: str
    period_start: datetime
    period_end: datetime
    message_stats: MessageStats
    time_stats: TimeStats
    category_stats: CategoryStats
    tag_stats: TagStats
    conversation_stats: ConversationStats
