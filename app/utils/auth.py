from database.database import async_get_db
from database.utils import get_user_by_api_key
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

API_KEY_HEADER = APIKeyHeader(name="api-key")


async def authenticate_user(
    api_key: str = Security(API_KEY_HEADER),
    session: AsyncSession = Depends(async_get_db),
):
    """Check if user exists otherwise raise errors"""
    user = await get_user_by_api_key(api_key, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key authentication failed",
            headers={"api-key": ""},
        )

    return user
