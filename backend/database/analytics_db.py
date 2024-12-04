from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    Float, 
    String, 
    DateTime, 
    JSON, 
    ForeignKey,
    Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

Base = declarative_base()

class AnalyticsUser(Base):
    __tablename__ = "analytics_users"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    conversations = relationship("Conversation", back_populates="user")
    analytics = relationship("UserAnalyticsData", back_populates="user", uselist=False)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("analytics_users.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    message_count = Column(Integer, default=0)
    category = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    avg_response_time = Column(Float, default=0.0)
    user = relationship("AnalyticsUser", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_user = Column(Boolean, default=True)
    content_length = Column(Integer)
    response_time = Column(Float, nullable=True)
    conversation = relationship("Conversation", back_populates="messages")

class UserAnalyticsData(Base):
    __tablename__ = "user_analytics"

    user_id = Column(String, ForeignKey("analytics_users.id"), primary_key=True)
    message_stats = Column(JSON, default=dict)
    time_stats = Column(JSON, default=dict)
    category_stats = Column(JSON, default=dict)
    tag_stats = Column(JSON, default=dict)
    conversation_stats = Column(JSON, default=dict)
    last_updated = Column(DateTime, default=datetime.utcnow)
    user = relationship("AnalyticsUser", back_populates="analytics")

class AnalyticsDB:
    def __init__(self, db_url: str = "sqlite:///./analytics.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    async def create_user(self, user_id: str) -> AnalyticsUser:
        with self.get_session() as session:
            user = AnalyticsUser(id=user_id)
            session.add(user)
            session.commit()
            return user

    async def get_user(self, user_id: str) -> Optional[AnalyticsUser]:
        with self.get_session() as session:
            return session.query(AnalyticsUser).filter(AnalyticsUser.id == user_id).first()

    async def create_conversation(self, user_id: str, conversation_id: str) -> Conversation:
        with self.get_session() as session:
            conv = Conversation(id=conversation_id, user_id=user_id)
            session.add(conv)
            session.commit()
            return conv

    async def add_message(self, conversation_id: str, is_user: bool, content_length: int, response_time: Optional[float] = None):
        with self.get_session() as session:
            msg = Message(
                conversation_id=conversation_id,
                is_user=is_user,
                content_length=content_length,
                response_time=response_time
            )
            session.add(msg)
            session.commit()

    async def update_conversation(self, conversation_id: str, **kwargs):
        with self.get_session() as session:
            conv = session.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                for key, value in kwargs.items():
                    setattr(conv, key, value)
                session.commit()

    async def update_user_analytics(self, user_id: str, analytics_data: Dict):
        with self.get_session() as session:
            analytics = session.query(UserAnalyticsData).filter(UserAnalyticsData.user_id == user_id).first()
            if not analytics:
                analytics = UserAnalyticsData(user_id=user_id)
                session.add(analytics)
            
            analytics.message_stats = analytics_data.get("message_stats", {})
            analytics.time_stats = analytics_data.get("time_stats", {})
            analytics.category_stats = analytics_data.get("category_stats", {})
            analytics.tag_stats = analytics_data.get("tag_stats", {})
            analytics.conversation_stats = analytics_data.get("conversation_stats", {})
            analytics.last_updated = datetime.utcnow()
            
            session.commit()

    async def get_user_analytics(self, user_id: str) -> Optional[Dict]:
        with self.get_session() as session:
            analytics = session.query(UserAnalyticsData).filter(UserAnalyticsData.user_id == user_id).first()
            if analytics:
                return {
                    "message_stats": analytics.message_stats,
                    "time_stats": analytics.time_stats,
                    "category_stats": analytics.category_stats,
                    "tag_stats": analytics.tag_stats,
                    "conversation_stats": analytics.conversation_stats,
                    "last_updated": analytics.last_updated.isoformat()
                }
            return None

    async def get_user_conversations(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Conversation]:
        with self.get_session() as session:
            query = session.query(Conversation).filter(Conversation.user_id == user_id)
            
            if start_date:
                query = query.filter(Conversation.start_time >= start_date)
            if end_date:
                query = query.filter(Conversation.start_time <= end_date)
                
            return query.all()

    async def cleanup_old_data(self, days: int = 30):
        cutoff = datetime.utcnow() - timedelta(days=days)
        with self.get_session() as session:
            session.query(Message).filter(Message.timestamp < cutoff).delete()
            session.query(Conversation).filter(Conversation.start_time < cutoff).delete()
            session.commit()
