import re
from fastapi import Header, HTTPException
from db.auth import check_user

def get_user(authorization: str = Header(None)) -> dict:
    """Middleware guard: Extract and validate Bearer token."""
    
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={"error": "Access token required"}
        )
    
    # Match "Bearer <token>" format
    match = re.match(r'^Bearer\s+(\S+)$', authorization)
    if not match:
        raise HTTPException(
            status_code=401,
            detail={"error": "Access token required"}
        )
    
    token = match.group(1)
    user = check_user(token)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": "Access token required"}
        )
    
    return user