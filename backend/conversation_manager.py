from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
import json
import os
from config import get_settings
from pydantic import BaseModel
import uuid
from conversation.models import Tag, Category, ConversationMetadata, ConversationUpdate

settings = get_settings()

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime

class Conversation(BaseModel):
    id: str
    messages: List[Message]
    metadata: ConversationMetadata
    last_updated: datetime
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in self.messages
            ],
            "metadata": self.metadata.dict(),
            "last_updated": self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Conversation':
        return cls(
            id=data["id"],
            messages=[
                Message(
                    role=msg["role"],
                    content=msg["content"],
                    timestamp=datetime.fromisoformat(msg["timestamp"])
                )
                for msg in data["messages"]
            ],
            metadata=ConversationMetadata(**data["metadata"]),
            last_updated=datetime.fromisoformat(data["last_updated"])
        )

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.tags: Dict[str, Tag] = {}
        self.categories: Dict[str, Category] = {}
        self._load_data()
    
    def _get_storage_path(self, filename: str) -> str:
        """Get the path to a storage file."""
        storage_dir = os.path.join(settings.CACHE_DIR, "conversations")
        os.makedirs(storage_dir, exist_ok=True)
        return os.path.join(storage_dir, filename)
    
    def _load_data(self):
        """Load all data from storage."""
        try:
            # Load conversations
            conv_path = self._get_storage_path("conversations.json")
            if os.path.exists(conv_path):
                with open(conv_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for conv_data in data.values():
                        conv = Conversation.from_dict(conv_data)
                        if datetime.now() - conv.last_updated < timedelta(seconds=settings.CONVERSATION_EXPIRY):
                            self.conversations[conv.id] = conv
            
            # Load tags
            tags_path = self._get_storage_path("tags.json")
            if os.path.exists(tags_path):
                with open(tags_path, 'r', encoding='utf-8') as f:
                    self.tags = {tag_id: Tag(**tag_data) 
                               for tag_id, tag_data in json.load(f).items()}
            
            # Load categories
            categories_path = self._get_storage_path("categories.json")
            if os.path.exists(categories_path):
                with open(categories_path, 'r', encoding='utf-8') as f:
                    self.categories = {cat_id: Category(**cat_data) 
                                    for cat_id, cat_data in json.load(f).items()}
                    
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def _save_data(self):
        """Save all data to storage."""
        try:
            # Save conversations
            conv_path = self._get_storage_path("conversations.json")
            with open(conv_path, 'w', encoding='utf-8') as f:
                json.dump(
                    {conv_id: conv.to_dict() for conv_id, conv in self.conversations.items()},
                    f,
                    ensure_ascii=False,
                    indent=2
                )
            
            # Save tags
            tags_path = self._get_storage_path("tags.json")
            with open(tags_path, 'w', encoding='utf-8') as f:
                json.dump(
                    {tag_id: tag.dict() for tag_id, tag in self.tags.items()},
                    f,
                    ensure_ascii=False,
                    indent=2
                )
            
            # Save categories
            categories_path = self._get_storage_path("categories.json")
            with open(categories_path, 'w', encoding='utf-8') as f:
                json.dump(
                    {cat_id: cat.dict() for cat_id, cat in self.categories.items()},
                    f,
                    ensure_ascii=False,
                    indent=2
                )
                
        except Exception as e:
            print(f"Error saving data: {str(e)}")
    
    def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        """Create a new conversation and return its ID."""
        conv_id = str(uuid.uuid4())
        now = datetime.now()
        
        self.conversations[conv_id] = Conversation(
            id=conv_id,
            messages=[],
            metadata=ConversationMetadata(
                user_id=user_id,
                title=title,
                created_at=now,
                last_accessed=now
            ),
            last_updated=now
        )
        self._save_data()
        return conv_id
    
    def add_message(self, conv_id: str, role: str, content: str) -> Optional[List[Message]]:
        """Add a message to a conversation and return updated message history."""
        if conv_id not in self.conversations:
            return None
            
        conv = self.conversations[conv_id]
        conv.messages.append(Message(
            role=role,
            content=content,
            timestamp=datetime.now()
        ))
        
        # Trim history if it exceeds maximum length
        if len(conv.messages) > settings.MAX_CONVERSATION_HISTORY:
            conv.messages = conv.messages[-settings.MAX_CONVERSATION_HISTORY:]
            
        conv.last_updated = datetime.now()
        conv.metadata.last_accessed = datetime.now()
        self._save_data()
        return conv.messages
    
    def get_conversation_history(self, conv_id: str) -> Optional[List[Message]]:
        """Get the message history for a conversation."""
        if conv_id not in self.conversations:
            return None
        return self.conversations[conv_id].messages
    
    def format_history_for_llm(self, conv_id: str) -> str:
        """Format conversation history for the LLM."""
        messages = self.get_conversation_history(conv_id)
        if not messages:
            return ""
            
        formatted = "Previous conversation:\n"
        for msg in messages:
            role_name = "User" if msg.role == "user" else "Assistant"
            formatted += f"{role_name}: {msg.content}\n"
        return formatted
    
    def update_conversation(self, conv_id: str, update: ConversationUpdate) -> bool:
        """Update conversation metadata."""
        if conv_id not in self.conversations:
            return False
            
        conv = self.conversations[conv_id]
        
        # Update fields if provided
        if update.category_id is not None:
            if update.category_id and update.category_id not in self.categories:
                return False
            conv.metadata.category_id = update.category_id
            
        if update.tags is not None:
            if len(update.tags) > settings.MAX_TAGS_PER_CONVERSATION:
                return False
            if not all(tag_id in self.tags for tag_id in update.tags):
                return False
            conv.metadata.tags = update.tags
            
        if update.title is not None:
            conv.metadata.title = update.title
            
        if update.description is not None:
            conv.metadata.description = update.description
            
        if update.is_shared is not None:
            conv.metadata.is_shared = update.is_shared
            
        if update.shared_with is not None:
            conv.metadata.shared_with = update.shared_with
            
        conv.last_updated = datetime.now()
        self._save_data()
        return True
    
    def create_tag(self, name: str, color: str, user_id: str) -> Optional[Tag]:
        """Create a new tag."""
        if len(name) > settings.MAX_TAG_LENGTH:
            return None
            
        tag_id = str(uuid.uuid4())
        tag = Tag(
            id=tag_id,
            name=name,
            color=color,
            created_at=datetime.now(),
            user_id=user_id
        )
        
        self.tags[tag_id] = tag
        self._save_data()
        return tag
    
    def create_category(self, name: str, description: Optional[str], user_id: str) -> Optional[Category]:
        """Create a new category."""
        if len(name) > settings.MAX_CATEGORY_NAME_LENGTH:
            return None
            
        # Check if user has reached maximum categories
        user_categories = sum(1 for cat in self.categories.values() if cat.user_id == user_id)
        if user_categories >= settings.MAX_CATEGORIES_PER_USER:
            return None
            
        category_id = str(uuid.uuid4())
        category = Category(
            id=category_id,
            name=name,
            description=description,
            created_at=datetime.now(),
            user_id=user_id
        )
        
        self.categories[category_id] = category
        self._save_data()
        return category
    
    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """Get all conversations for a user."""
        return [
            conv for conv in self.conversations.values()
            if conv.metadata.user_id == user_id or user_id in conv.metadata.shared_with
        ]
    
    def get_user_tags(self, user_id: str) -> List[Tag]:
        """Get all tags created by a user."""
        return [tag for tag in self.tags.values() if tag.user_id == user_id]
    
    def get_user_categories(self, user_id: str) -> List[Category]:
        """Get all categories created by a user."""
        return [cat for cat in self.categories.values() if cat.user_id == user_id]
    
    def cleanup_expired_conversations(self):
        """Remove expired conversations."""
        current_time = datetime.now()
        expired_ids = [
            conv_id for conv_id, conv in self.conversations.items()
            if (current_time - conv.last_updated).total_seconds() > settings.CONVERSATION_EXPIRY
        ]
        
        for conv_id in expired_ids:
            del self.conversations[conv_id]
            
        if expired_ids:
            self._save_data()
