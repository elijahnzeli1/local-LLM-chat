from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class MessageStats(BaseModel):
    total_messages: int = Field(default=0)
    user_messages: int = Field(default=0)
    assistant_messages: int = Field(default=0)
    avg_user_length: float = Field(default=0.0)
    avg_assistant_length: float = Field(default=0.0)

class TimeStats(BaseModel):
    hour_distribution: Dict[int, int] = Field(default_factory=dict)
    day_distribution: Dict[int, int] = Field(default_factory=dict)
    avg_response_time: float = Field(default=0.0)

class CategoryStats(BaseModel):
    category_distribution: Dict[str, int] = Field(default_factory=dict)
    most_used_category: Optional[str] = None

class TagStats(BaseModel):
    tag_distribution: Dict[str, int] = Field(default_factory=dict)
    most_used_tags: List[str] = Field(default_factory=list)

class ConversationStats(BaseModel):
    total_conversations: int = Field(default=0)
    active_conversations: int = Field(default=0)
    avg_messages_per_conversation: float = Field(default=0.0)
    avg_conversation_length: float = Field(default=0.0)
    active_today: int = Field(default=0)
    average_length: float = Field(default=0.0)
    average_duration: float = Field(default=0.0)

class UserAnalytics(BaseModel):
    user_id: str
    message_stats: MessageStats = Field(default_factory=MessageStats)
    time_stats: TimeStats = Field(default_factory=TimeStats)
    category_stats: CategoryStats = Field(default_factory=CategoryStats)
    tag_stats: TagStats = Field(default_factory=TagStats)
    conversation_stats: ConversationStats = Field(default_factory=ConversationStats)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class AnalyticsUpdate(BaseModel):
    conversation_id: str
    user_id: str
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    message_count: int = Field(default=1)
    user_message_length: Optional[int] = None
    assistant_message_length: Optional[int] = None
    response_time: Optional[float] = None
    conversation_duration: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
