from pydantic import BaseModel


class ErrorResponse(BaseModel):
    result: bool = False
    error_type: str
    error_message: str
