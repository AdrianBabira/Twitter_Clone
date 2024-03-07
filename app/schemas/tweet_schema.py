from typing import List, Optional

from models.likes import Like as LikeModel
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from .base_schema import DefaultSchema
from .media_schema import Media
from .user_schema import DefaultUser


class Like(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
    user_id: int
    username: str = Field(alias="name")

    @model_validator(mode="before")
    @classmethod
    def validate_model(self, data: LikeModel) -> "Like":
        """Field username does not actually exist on our model, because
        it is  a relationship to the user, we have to construct the model"""
        return Like.model_construct(
            user_id=data.user_id, username=data.user.username
        )


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = list()


class TweetCreate(DefaultSchema):
    tweet_id: int


class Tweet(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
    id: int
    tweet_data: str = Field(alias="content")
    media: List = Field(alias="attachments")
    user: DefaultUser = Field(alias="author")
    likes: List[Like]

    @field_validator("media", mode="after")
    @classmethod
    def extract_attachments(cls, values: List[Media]):
        return [value.media_path for value in values]


class TweetOut(DefaultSchema):
    tweets: List[Tweet]
