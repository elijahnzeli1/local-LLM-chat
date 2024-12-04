from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from .models import (
    MessageStats, TimeStats, CategoryStats,
    TagStats, ConversationStats, UserAnalytics
)
from ..conversation_manager import ConversationManager
from ..conversation.models import Conversation, Message
import statistics

class AnalyticsManager:
    def __init__(self, conversation_manager: ConversationManager):
        self.conversation_manager = conversation_manager
        
    def _calculate_message_stats(self, messages: List[Message]) -> MessageStats:
        """Calculate message statistics."""
        if not messages:
            return MessageStats(
                total_messages=0,
                user_messages=0,
                assistant_messages=0,
                avg_user_length=0,
                avg_assistant_length=0
            )
            
        user_lengths = [len(msg.content) for msg in messages if msg.role == "user"]
        assistant_lengths = [len(msg.content) for msg in messages if msg.role == "assistant"]
        
        return MessageStats(
            total_messages=len(messages),
            user_messages=len(user_lengths),
            assistant_messages=len(assistant_lengths),
            avg_user_length=statistics.mean(user_lengths) if user_lengths else 0,
            avg_assistant_length=statistics.mean(assistant_lengths) if assistant_lengths else 0
        )
        
    def _calculate_time_stats(self, messages: List[Message]) -> TimeStats:
        """Calculate time-based statistics."""
        hour_dist = defaultdict(int)
        day_dist = defaultdict(int)
        response_times = []
        
        for i, msg in enumerate(messages):
            hour = msg.timestamp.hour
            day = msg.timestamp.weekday()
            hour_dist[hour] += 1
            day_dist[day] += 1
            
            # Calculate response time if this is an assistant message
            if msg.role == "assistant" and i > 0 and messages[i-1].role == "user":
                response_time = (msg.timestamp - messages[i-1].timestamp).total_seconds()
                response_times.append(response_time)
                
        return TimeStats(
            hour_distribution=dict(hour_dist),
            day_distribution=dict(day_dist),
            avg_response_time=statistics.mean(response_times) if response_times else 0
        )
        
    def _calculate_category_stats(self, conversations: List[Conversation]) -> CategoryStats:
        """Calculate category statistics."""
        category_dist = defaultdict(int)
        
        for conv in conversations:
            if conv.metadata.category_id:
                category = self.conversation_manager.categories.get(conv.metadata.category_id)
                if category:
                    category_dist[category.name] += 1
                    
        most_used = max(category_dist.items(), key=lambda x: x[1])[0] if category_dist else None
        
        return CategoryStats(
            category_distribution=dict(category_dist),
            most_used_category=most_used
        )
        
    def _calculate_tag_stats(self, conversations: List[Conversation]) -> TagStats:
        """Calculate tag statistics."""
        tag_dist = defaultdict(int)
        
        for conv in conversations:
            for tag_id in conv.metadata.tags:
                tag = self.conversation_manager.tags.get(tag_id)
                if tag:
                    tag_dist[tag.name] += 1
                    
        # Get top 5 tags
        top_tags = sorted(tag_dist.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return TagStats(
            tag_distribution=dict(tag_dist),
            most_used_tags=[tag for tag, _ in top_tags]
        )
        
    def _calculate_conversation_stats(self, conversations: List[Conversation]) -> ConversationStats:
        """Calculate conversation statistics."""
        if not conversations:
            return ConversationStats(
                total_conversations=0,
                active_conversations=0,
                avg_messages_per_conversation=0,
                avg_conversation_length=0
            )
            
        now = datetime.now()
        active_convs = [
            conv for conv in conversations
            if (now - conv.last_updated).total_seconds() < 24 * 60 * 60  # Active in last 24h
        ]
        
        msg_counts = [len(conv.messages) for conv in conversations]
        conv_lengths = [
            (conv.last_updated - conv.metadata.created_at).total_seconds() / 60
            for conv in conversations
        ]
        
        return ConversationStats(
            total_conversations=len(conversations),
            active_conversations=len(active_convs),
            avg_messages_per_conversation=statistics.mean(msg_counts) if msg_counts else 0,
            avg_conversation_length=statistics.mean(conv_lengths) if conv_lengths else 0
        )
        
    def get_user_analytics(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> UserAnalytics:
        """Get analytics for a specific user within the given time period."""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)  # Last 30 days by default
        if not end_date:
            end_date = datetime.now()
            
        # Get user's conversations
        all_conversations = self.conversation_manager.get_user_conversations(user_id)
        
        # Filter conversations by date range
        conversations = [
            conv for conv in all_conversations
            if start_date <= conv.metadata.created_at <= end_date
        ]
        
        # Get all messages from filtered conversations
        all_messages = []
        for conv in conversations:
            all_messages.extend(conv.messages)
            
        # Sort messages by timestamp
        all_messages.sort(key=lambda x: x.timestamp)
        
        return UserAnalytics(
            user_id=user_id,
            period_start=start_date,
            period_end=end_date,
            message_stats=self._calculate_message_stats(all_messages),
            time_stats=self._calculate_time_stats(all_messages),
            category_stats=self._calculate_category_stats(conversations),
            tag_stats=self._calculate_tag_stats(conversations),
            conversation_stats=self._calculate_conversation_stats(conversations)
        )
