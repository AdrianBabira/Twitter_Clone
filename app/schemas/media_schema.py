from pydantic import BaseModel, Field

from .base_schema import ConfigDict, DefaultSchema


class MediaUpload(DefaultSchema):
    id: int = Field(alias="media_id")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class Media(BaseModel):
    media_path: str
