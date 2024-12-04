from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.analytics import (
    UserAnalytics,
    AnalyticsUpdate,
    MessageStats,
    TimeStats,
    CategoryStats,
    TagStats,
    ConversationStats,
)
from database.analytics_db import AnalyticsDB

class AnalyticsService:
    def __init__(self):
        self.db = AnalyticsDB()

    async def get_user_analytics(self, user_id: str) -> UserAnalytics:
        """Get analytics for a specific user, creating if not exists."""
        analytics_data = await self.db.get_user_analytics(user_id)
        if not analytics_data:
            # Create new user and analytics
            await self.db.create_user(user_id)
            return UserAnalytics(user_id=user_id)
        
        return UserAnalytics(
            user_id=user_id,
            message_stats=MessageStats(**analytics_data["message_stats"]),
            time_stats=TimeStats(**analytics_data["time_stats"]),
            category_stats=CategoryStats(**analytics_data["category_stats"]),
            tag_stats=TagStats(**analytics_data["tag_stats"]),
            conversation_stats=ConversationStats(**analytics_data["conversation_stats"]),
            last_updated=datetime.fromisoformat(analytics_data["last_updated"])
        )

    async def update_analytics(self, update: AnalyticsUpdate):
        """Update analytics based on new conversation data."""
        analytics = await self.get_user_analytics(update.user_id)
        
        # Update message stats
        if update.user_message_length is not None:
            self._update_message_stats(analytics.message_stats, 
                                    update.user_message_length, 
                                    update.assistant_message_length)

        # Update time stats
        if update.response_time is not None:
            self._update_time_stats(analytics.time_stats, 
                                  update.timestamp, 
                                  update.response_time)

        # Update category stats
        if update.category:
            self._update_category_stats(analytics.category_stats, update.category)

        # Update tag stats
        if update.tags:
            self._update_tag_stats(analytics.tag_stats, update.tags)

        # Update conversation stats
        self._update_conversation_stats(analytics.conversation_stats, 
                                      update.conversation_duration,
                                      update.message_count)

        analytics.last_updated = datetime.utcnow()

        # Save to database
        await self.db.update_user_analytics(update.user_id, analytics.dict())
        
        # Update conversation in database
        await self.db.update_conversation(
            update.conversation_id,
            category=update.category,
            tags=update.tags,
            message_count=update.message_count,
            end_time=update.timestamp if update.conversation_duration is not None else None
        )

        # Add message to database
        if update.user_message_length is not None:
            await self.db.add_message(
                update.conversation_id,
                is_user=True,
                content_length=update.user_message_length
            )
        if update.assistant_message_length is not None:
            await self.db.add_message(
                update.conversation_id,
                is_user=False,
                content_length=update.assistant_message_length,
                response_time=update.response_time
            )

    def _update_message_stats(self, stats: MessageStats, 
                            user_length: Optional[int], 
                            assistant_length: Optional[int]):
        """Update message statistics."""
        stats.total_messages += 1
        
        if user_length is not None:
            stats.user_messages += 1
            new_avg = ((stats.avg_user_length * (stats.user_messages - 1)) + user_length) / stats.user_messages
            stats.avg_user_length = new_avg

        if assistant_length is not None:
            stats.assistant_messages += 1
            new_avg = ((stats.avg_assistant_length * (stats.assistant_messages - 1)) + assistant_length) / stats.assistant_messages
            stats.avg_assistant_length = new_avg

    def _update_time_stats(self, stats: TimeStats, 
                          timestamp: datetime, 
                          response_time: float):
        """Update time-based statistics."""
        hour = timestamp.hour
        day = timestamp.weekday()

        stats.hour_distribution[hour] = stats.hour_distribution.get(hour, 0) + 1
        stats.day_distribution[day] = stats.day_distribution.get(day, 0) + 1

        # Update average response time
        total_messages = sum(stats.hour_distribution.values())
        stats.avg_response_time = (
            (stats.avg_response_time * (total_messages - 1) + response_time) / total_messages
        )

    def _update_category_stats(self, stats: CategoryStats, category: str):
        """Update category statistics."""
        stats.category_distribution[category] = stats.category_distribution.get(category, 0) + 1
        
        # Update most used category
        if (stats.most_used_category is None or 
            stats.category_distribution[category] > 
            stats.category_distribution[stats.most_used_category]):
            stats.most_used_category = category

    def _update_tag_stats(self, stats: TagStats, tags: List[str]):
        """Update tag statistics."""
        for tag in tags:
            stats.tag_distribution[tag] = stats.tag_distribution.get(tag, 0) + 1

        # Update most used tags (top 5)
        stats.most_used_tags = sorted(
            stats.tag_distribution.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

    def _update_conversation_stats(self, stats: ConversationStats, 
                                 duration: Optional[float],
                                 message_count: int):
        """Update conversation statistics."""
        stats.total_conversations += 1
        
        # Update active conversations (last 24 hours)
        stats.active_today += 1

        # Update average messages per conversation
        stats.avg_messages_per_conversation = (
            (stats.avg_messages_per_conversation * (stats.total_conversations - 1) + message_count)
            / stats.total_conversations
        )

        if duration is not None:
            # Update average duration
            stats.average_duration = (
                (stats.average_duration * (stats.total_conversations - 1) + duration)
                / stats.total_conversations
            )

        # Update average length
        stats.average_length = stats.avg_messages_per_conversation

    async def get_advanced_analytics(self, user_id: str, days: int = 30) -> Dict:
        """Get advanced analytics for visualization."""
        start_date = datetime.utcnow() - timedelta(days=days)
        conversations = await self.db.get_user_conversations(user_id, start_date)
        
        # Time series data
        daily_counts = {}
        response_times = []
        message_lengths = []
        category_trends = {}
        
        for conv in conversations:
            date_key = conv.start_time.date().isoformat()
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
            
            if conv.avg_response_time:
                response_times.append(conv.avg_response_time)
                
            if conv.category:
                category_trends[conv.category] = category_trends.get(conv.category, 0) + 1
            
            for msg in conv.messages:
                message_lengths.append(msg.content_length)
        
        return {
            "time_series": {
                "daily_conversation_counts": daily_counts,
                "avg_response_time_trend": sum(response_times) / len(response_times) if response_times else 0,
                "avg_message_length_trend": sum(message_lengths) / len(message_lengths) if message_lengths else 0
            },
            "category_trends": category_trends,
            "usage_patterns": {
                "total_conversations": len(conversations),
                "active_days": len(daily_counts),
                "peak_day": max(daily_counts.items(), key=lambda x: x[1])[0] if daily_counts else None
            }
        }

    async def cleanup_old_analytics(self, days: int = 30):
        """Remove analytics older than specified days."""
        await self.db.cleanup_old_data(days)
