from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app.config import jwt_settings


def generate_expiration(user_role: str) -> timedelta:
    if user_role == "user":
        return timedelta(days=7)
    else:
        return timedelta(minutes=jwt_settings.access_token_expire_minutes)


def generate_payload(user) -> Dict[str, Any]:
    return {
        "sub": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
    }


def create_access_token(data: Dict[str, Any]):
    to_encode = data.copy()
    expire = datetime.utcnow() + generate_expiration(user_role=data["role"])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
    )
    return encoded_jwt


def jwt_validate(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            jwt_settings.secret_key,
            algorithms=[jwt_settings.algorithm],
        )
        return payload
    except InvalidTokenError as e:
        print(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail=str(e))
