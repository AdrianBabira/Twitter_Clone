from contextlib import asynccontextmanager

import uvicorn
from database.database import async_get_db, engine
from database.utils import create_test_user_if_not_exist, init_models
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from routers import media, tweets, users
from starlette.exceptions import HTTPException
from utils.exceptions import (
    custom_http_exception_handler,
    response_validation_exception_handler,
    validation_exception_handler,
)

session = async_get_db()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    await init_models()
    await create_test_user_if_not_exist(await anext(session))

    yield
    if engine is not None:
        await engine.dispose()


app = FastAPI(lifespan=lifespan, debug=True, docs_url="/docs")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(
    ResponseValidationError, response_validation_exception_handler
)


app.include_router(media.router)
app.include_router(users.router)
app.include_router(tweets.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
