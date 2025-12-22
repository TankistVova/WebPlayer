from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

VALID_TOKEN = "video-player-token-2024"


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(401, "Неверный токен")
    return credentials.credentials