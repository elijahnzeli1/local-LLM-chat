from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from .models import UserInDB, TokenData
import uuid
import json
import os
from config import get_settings

settings = get_settings()

class AuthHandler:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.users_file = os.path.join(settings.CACHE_DIR, "users.json")
        self._ensure_users_file()

    def _ensure_users_file(self):
        """Ensure the users file exists."""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _load_users(self):
        """Load users from file."""
        with open(self.users_file, 'r') as f:
            return json.load(f)

    def _save_users(self, users):
        """Save users to file."""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def get_user(self, username: str) -> Optional[UserInDB]:
        users = self._load_users()
        if username in users:
            user_data = users[username]
            return UserInDB(**user_data)
        return None

    async def create_user(self, username: str, email: str, password: str) -> UserInDB:
        users = self._load_users()
        if username in users:
            raise ValueError("Username already registered")

        user_dict = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "hashed_password": self.get_password_hash(password),
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }

        users[username] = user_dict
        self._save_users(users)
        return UserInDB(**user_dict)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user = self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def verify_token(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            return TokenData(username=username)
        except JWTError:
            return None
