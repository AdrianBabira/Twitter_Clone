from http.client import responses

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from schemas.exception_schema import ErrorResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    error_type = "ValidationError"
    error_schema = ErrorResponse(
        error_type=error_type, error_message=repr(exc)
    )
    return JSONResponse(
        error_schema.model_dump(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def response_validation_exception_handler(
    request: Request, exc: ResponseValidationError
):
    error_type = "ResponseValidationError"
    error_schema = ErrorResponse(
        error_type=error_type, error_message=repr(exc.errors())
    )
    return JSONResponse(
        error_schema.model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def custom_http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    error_schema = ErrorResponse(
        error_type=responses[exc.status_code], error_message=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code, content=error_schema.model_dump()
    )
