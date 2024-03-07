from pydantic import BaseModel, ConfigDict


class DefaultSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: bool = True
