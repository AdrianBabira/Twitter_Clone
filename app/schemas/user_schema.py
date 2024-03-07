from typing import List

from pydantic import BaseModel, ConfigDict, Field

from .base_schema import DefaultSchema


class DefaultUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    username: str = Field(alias="name")


class User(DefaultUser):
    model_config = ConfigDict(from_attributes=True)
    followers: List[DefaultUser]
    following: List[DefaultUser]


class UserOutSchema(DefaultSchema):
    user: User
