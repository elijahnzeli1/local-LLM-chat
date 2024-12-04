from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth_handler import AuthHandler
from .models import User, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_handler = AuthHandler()

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = auth_handler.verify_token(token)
    if token_data is None:
        raise credentials_exception
        
    user = auth_handler.get_user(token_data.username)
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
