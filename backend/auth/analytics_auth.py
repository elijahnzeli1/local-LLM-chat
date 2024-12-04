from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Optional
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel

class AnalyticsAuth:
    def __init__(self, secret_key: str = "your-secret-key"):
        self.secret_key = secret_key
        self.api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

    async def get_api_key(self, api_key_header: str = Security(APIKeyHeader(name="X-API-Key"))) -> str:
        if not api_key_header:
            raise HTTPException(
                status_code=401,
                detail="Could not validate API key"
            )
        return api_key_header

    async def verify_api_key(self, api_key: str = Depends(get_api_key)) -> bool:
        """Verify if the API key is valid."""
        try:
            payload = jwt.decode(api_key, self.secret_key, algorithms=["HS256"])
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(
                    status_code=401,
                    detail="API key has expired"
                )
            return True
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )

    def create_api_key(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new API key for a user."""
        if expires_delta is None:
            expires_delta = timedelta(days=30)

        expire = datetime.utcnow() + expires_delta
        to_encode = {
            "sub": user_id,
            "exp": expire.timestamp(),
            "iat": datetime.utcnow().timestamp()
        }
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256")

    def get_current_user(self, api_key: str = Depends(get_api_key)) -> str:
        """Get the current user from the API key."""
        try:
            payload = jwt.decode(api_key, self.secret_key, algorithms=["HS256"])
            return payload["sub"]
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate API key"
            )

analytics_auth = AnalyticsAuth()
