from typing import Annotated

from database.database import async_get_db
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from models.media import Media
from models.users import User
from schemas.media_schema import MediaUpload
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import authenticate_user
from utils.file_utils import save_uploaded_file

router = APIRouter(prefix="/api", tags=["media_v1"])


@router.post(
    "/medias", status_code=status.HTTP_201_CREATED, response_model=MediaUpload
)
async def upload_media(
    file: UploadFile,
    user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(async_get_db),
):
    try:
        file = await save_uploaded_file(file)
        new_media = Media(media_path=file)
        session.add(new_media)
        await session.commit()

        return new_media
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        )
