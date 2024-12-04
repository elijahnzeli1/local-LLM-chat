from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel
from .models import ConversationMetadata
import json
import os
from config import get_settings

settings = get_settings()

class ShareInvite(BaseModel):
    id: str
    conversation_id: str
    from_user_id: str
    to_user_id: str
    created_at: datetime
    expires_at: datetime
    accepted: bool = False
    
class SharingManager:
    def __init__(self):
        self.invites: Dict[str, ShareInvite] = {}
        self._load_invites()
        
    def _get_invites_path(self) -> str:
        storage_dir = os.path.join(settings.CACHE_DIR, "conversations")
        os.makedirs(storage_dir, exist_ok=True)
        return os.path.join(storage_dir, "share_invites.json")
        
    def _load_invites(self):
        try:
            path = self._get_invites_path()
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for invite_data in data.values():
                        invite_data['created_at'] = datetime.fromisoformat(invite_data['created_at'])
                        invite_data['expires_at'] = datetime.fromisoformat(invite_data['expires_at'])
                        self.invites[invite_data['id']] = ShareInvite(**invite_data)
        except Exception as e:
            print(f"Error loading invites: {str(e)}")
            
    def _save_invites(self):
        try:
            path = self._get_invites_path()
            with open(path, 'w', encoding='utf-8') as f:
                data = {
                    invite.id: {
                        **invite.dict(),
                        'created_at': invite.created_at.isoformat(),
                        'expires_at': invite.expires_at.isoformat()
                    }
                    for invite in self.invites.values()
                }
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving invites: {str(e)}")
            
    def create_invite(self, conversation_id: str, from_user_id: str, to_user_id: str) -> Optional[ShareInvite]:
        """Create a new share invite."""
        from uuid import uuid4
        
        # Check if invite already exists
        existing = [
            inv for inv in self.invites.values()
            if inv.conversation_id == conversation_id
            and inv.to_user_id == to_user_id
            and not inv.accepted
            and inv.expires_at > datetime.now()
        ]
        
        if existing:
            return existing[0]
            
        invite = ShareInvite(
            id=str(uuid4()),
            conversation_id=conversation_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            created_at=datetime.now(),
            expires_at=datetime.now() + settings.SHARE_INVITE_EXPIRY,
            accepted=False
        )
        
        self.invites[invite.id] = invite
        self._save_invites()
        return invite
        
    def accept_invite(self, invite_id: str, user_id: str) -> bool:
        """Accept a share invite."""
        if invite_id not in self.invites:
            return False
            
        invite = self.invites[invite_id]
        if (invite.to_user_id != user_id
            or invite.accepted
            or invite.expires_at < datetime.now()):
            return False
            
        invite.accepted = True
        self._save_invites()
        return True
        
    def get_pending_invites(self, user_id: str) -> List[ShareInvite]:
        """Get all pending invites for a user."""
        now = datetime.now()
        return [
            inv for inv in self.invites.values()
            if inv.to_user_id == user_id
            and not inv.accepted
            and inv.expires_at > now
        ]
        
    def cleanup_expired_invites(self):
        """Remove expired invites."""
        now = datetime.now()
        expired = [
            invite_id for invite_id, invite in self.invites.items()
            if invite.expires_at < now and not invite.accepted
        ]
        
        for invite_id in expired:
            del self.invites[invite_id]
            
        if expired:
            self._save_invites()
