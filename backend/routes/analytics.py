from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional
from datetime import datetime, timedelta

from models.analytics import (
    UserAnalytics,
    AnalyticsUpdate,
    MessageStats,
    TimeStats,
    CategoryStats,
    TagStats,
    ConversationStats,
)
from analytics.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])
analytics_service = AnalyticsService()

@router.get("/user/{user_id}")
async def get_user_analytics(user_id: str) -> UserAnalytics:
    """Get analytics for a specific user."""
    return analytics_service.get_user_analytics(user_id)

@router.post("/update")
async def update_analytics(update: AnalyticsUpdate):
    """Update analytics with new conversation data."""
    try:
        analytics_service.update_analytics(update)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/messages")
async def get_message_stats(user_id: str) -> MessageStats:
    """Get message statistics for a user."""
    analytics = analytics_service.get_user_analytics(user_id)
    return analytics.message_stats

@router.get("/user/{user_id}/time")
async def get_time_stats(user_id: str) -> TimeStats:
    """Get time-based statistics for a user."""
    analytics = analytics_service.get_user_analytics(user_id)
    return analytics.time_stats

@router.get("/user/{user_id}/categories")
async def get_category_stats(user_id: str) -> CategoryStats:
    """Get category statistics for a user."""
    analytics = analytics_service.get_user_analytics(user_id)
    return analytics.category_stats

@router.get("/user/{user_id}/tags")
async def get_tag_stats(user_id: str) -> TagStats:
    """Get tag statistics for a user."""
    analytics = analytics_service.get_user_analytics(user_id)
    return analytics.tag_stats

@router.get("/user/{user_id}/conversations")
async def get_conversation_stats(
    user_id: str,
    include_previous: bool = False
) -> Dict[str, ConversationStats]:
    """Get conversation statistics for a user."""
    analytics = analytics_service.get_user_analytics(user_id)
    
    result = {
        "current": analytics.conversation_stats
    }
    
    if include_previous:
        # Calculate previous period stats (last 24 hours vs previous 24 hours)
        # This would typically come from a database, but we'll use a placeholder
        previous_stats = ConversationStats(
            total_conversations=analytics.conversation_stats.total_conversations - analytics.conversation_stats.active_today,
            active_conversations=analytics.conversation_stats.active_today,
            avg_messages_per_conversation=analytics.conversation_stats.avg_messages_per_conversation,
            avg_conversation_length=analytics.conversation_stats.avg_conversation_length,
            active_today=0,  # Previous period
            average_length=analytics.conversation_stats.average_length,
            average_duration=analytics.conversation_stats.average_duration
        )
        result["previous"] = previous_stats
    
    return result

@router.post("/cleanup")
async def cleanup_analytics(days: int = 30):
    """Clean up old analytics data."""
    try:
        analytics_service.cleanup_old_analytics(days)
        return {"status": "success", "message": f"Cleaned up analytics older than {days} days"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
