import re
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials as HTTPAuthCredentials
from db.auth import check_user

security = HTTPBearer()

def get_user(credentials: HTTPAuthCredentials = Depends(security)) -> dict:
    """Middleware guard: Extract and validate Bearer token."""
    
    token = credentials.credentials
    user = check_user(token)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": "Access token required"}
        )
    
    return user
