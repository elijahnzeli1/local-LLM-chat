from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
import json
import os
from config import get_settings
from pydantic import BaseModel
import uuid
from conversation.models import Tag, Category, ConversationMetadata, ConversationUpdate
import asyncio

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

class InternetResearch:
    async def search_and_analyze(self, query: str) -> Dict:
        # Implement internet research logic here
        # For demonstration purposes, return a dummy result
        return {
            "success": True,
            "results": [
                {"title": "Result 1", "url": "https://example.com/result1"},
                {"title": "Result 2", "url": "https://example.com/result2"}
            ]
        }

    def format_research_for_llm(self, results: Dict) -> str:
        # Implement formatting logic here
        # For demonstration purposes, return a dummy formatted string
        return "Here are some search results:\n" + "\n".join([f"{result['title']}: {result['url']}" for result in results["results"]])

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.tags: Dict[str, Tag] = {}
        self.categories: Dict[str, Category] = {}
        self.internet_research = InternetResearch()
        self._load_data()

    def _get_storage_path(self, filename: str):
        storage_dir = settings.storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        return os.path.join(storage_dir, filename)

    def _load_data(self):
        try:
            conversations_path = self._get_storage_path('conversations.json')
            if os.path.exists(conversations_path):
                with open(conversations_path, 'r') as f:
                    data = json.load(f)
                    self.conversations = {
                        conv_id: Conversation.from_dict(conv_data)
                        for conv_id, conv_data in data.items()
                    }
        except Exception as e:
            print(f"Error loading conversations: {e}")

    def _save_data(self):
        try:
            conversations_path = self._get_storage_path('conversations.json')
            with open(conversations_path, 'w') as f:
                json.dump(
                    {conv_id: conv.to_dict() for conv_id, conv in self.conversations.items()},
                    f,
                    indent=2
                )
        except Exception as e:
            print(f"Error saving conversations: {e}")

    def create_conversation(self, user_id: str, title: Optional[str] = None, mode: str = 'normal') -> str:
        conv_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        metadata = ConversationMetadata(
            title=title or ("New Project" if mode == "coding" else "New Chat"),
            created_by=user_id,
            created_at=now,
            last_updated=now,
            mode=mode
        )
        
        self.conversations[conv_id] = Conversation(
            id=conv_id,
            messages=[],
            metadata=metadata,
            last_updated=now
        )
        
        self._save_data()
        return conv_id

    async def add_message_with_context(
        self,
        conv_id: str,
        role: str,
        content: str,
        use_internet: bool = False
    ) -> List[Message]:
        """Add a message with optional internet research context"""
        if conv_id not in self.conversations:
            raise ValueError(f"Conversation {conv_id} not found")

        conversation = self.conversations[conv_id]
        now = datetime.utcnow()

        # Perform internet research if enabled
        research_context = ""
        if use_internet and role == "user":
            try:
                research_results = await self.internet_research.search_and_analyze(content)
                if research_results["success"]:
                    research_context = self.internet_research.format_research_for_llm(research_results)
            except Exception as e:
                print(f"Error performing internet research: {str(e)}")

        # Add research context as a system message if available
        if research_context:
            system_message = Message(
                role="system",
                content=research_context,
                timestamp=now
            )
            conversation.messages.append(system_message)

        # Add the user's message
        message = Message(
            role=role,
            content=content,
            timestamp=now
        )
        conversation.messages.append(message)
        conversation.last_updated = now
        conversation.metadata.last_updated = now

        self._save_data()
        return conversation.messages

    def add_message(self, conv_id: str, role: str, content: str) -> List[Message]:
        if conv_id not in self.conversations:
            raise ValueError(f"Conversation {conv_id} not found")
        
        now = datetime.utcnow()
        message = Message(role=role, content=content, timestamp=now)
        
        conversation = self.conversations[conv_id]
        conversation.messages.append(message)
        conversation.last_updated = now
        conversation.metadata.last_updated = now
        
        self._save_data()
        return conversation.messages

    def get_conversation_history(self, conv_id: str) -> List[Message]:
        if conv_id not in self.conversations:
            raise ValueError(f"Conversation {conv_id} not found")
        return self.conversations[conv_id].messages

    def format_history_for_llm(self, conv_id: str) -> List[Dict[str, str]]:
        if conv_id not in self.conversations:
            raise ValueError(f"Conversation {conv_id} not found")
            
        conversation = self.conversations[conv_id]
        formatted_messages = []
        
        # Add system message for coding mode
        if conversation.metadata.mode == 'coding':
            formatted_messages.append({
                "role": "system",
                "content": """You are an expert software developer assistant. Help users create applications step by step:
1. Understand requirements and suggest tech stack
2. Create project structure and setup
3. Implement features incrementally
4. Handle errors and debugging
5. Optimize and refactor code
6. Test and document the application

Use WebContainers to create, edit, and run code in real-time. Always explain your actions and next steps."""
            })
        
        # Add conversation messages
        formatted_messages.extend([
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ])
        
        return formatted_messages

    def update_conversation(self, conv_id: str, update: ConversationUpdate) -> None:
        if conv_id not in self.conversations:
            raise ValueError(f"Conversation {conv_id} not found")
            
        conversation = self.conversations[conv_id]
        
        if update.title is not None:
            conversation.metadata.title = update.title
        if update.description is not None:
            conversation.metadata.description = update.description
        if update.tags is not None:
            conversation.metadata.tags = update.tags
        if update.category is not None:
            conversation.metadata.category = update.category
            
        conversation.metadata.last_updated = datetime.utcnow()
        self._save_data()

    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """Get all conversations for a user."""
        return [
            conv for conv in self.conversations.values()
            if conv.metadata.created_by == user_id
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
