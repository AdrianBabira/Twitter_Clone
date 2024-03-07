import os
from collections.abc import AsyncGenerator
from typing import Dict, Mapping

import pytest
import pytest_asyncio
from database.database import Base
from database.database import async_get_db as get_db_session
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from main import app
from models.tweets import Tweet
from models.users import User
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

TEST_USERNAME = os.environ.get("USERNAME")
TEST_API_KEY = os.environ.get("API_KEY")
TEST_SERVER_PORT = os.environ.get("SERVER_PORT")

unauthorized_structure_response: Dict = {
    "result": False,
    "error_type": "Unauthorized",
    "error_message": "API key authentication failed",
}


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    DATABASE_URL = (
        f'postgresql+asyncpg://{os.environ.get("DB_USERNAME")}:'
        f'{os.environ.get("DB_PASSWORD")}@'
        f'{os.environ.get("DB_HOST")}'
        f':5432/{os.environ.get("DB_NAME")}'
    )
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        test_user = User(api_key=TEST_API_KEY, username=TEST_USERNAME)
        session.add(test_user)
        fake_users = [
            User(api_key=f"fake_api_key{i}", username=f"fake_user{i}")
            for i in range(1, 6)
        ]
        session.add_all(fake_users)
        yield session
        await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db_session] = lambda: db_session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a http client."""
    test_headers: Mapping[str, str] = {"api-key": "unauthorized"}
    if TEST_API_KEY is not None:
        test_headers = {"api-key": TEST_API_KEY}
    async with AsyncClient(
        app=test_app,
        base_url=f"http://localhost:{TEST_SERVER_PORT}/api",
        headers=test_headers,
    ) as client:
        yield client


@pytest_asyncio.fixture()
async def invalid_client(
    test_app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    test_headers: Mapping[str, str] = {"api-key": "unauthorized"}
    async with AsyncClient(
        app=test_app,
        base_url=f"http://localhost:{TEST_SERVER_PORT}/api",
        headers=test_headers,
    ) as client:
        yield client


@pytest_asyncio.fixture()
async def create_random_tweets(
    client: AsyncClient, faker: Faker, db_session: AsyncSession
):
    for user_id in range(2, 6):
        new_tweet = Tweet(
            user_id=user_id,
            tweet_data=faker.sentence(),
        )
        db_session.add(new_tweet)
