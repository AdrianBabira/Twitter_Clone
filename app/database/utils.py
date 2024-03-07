from typing import List

from database.database import async_get_db, engine
from fastapi import Depends, HTTPException, status
from models.media import Media
from models.users import Base, Like, Tweet, User
from sqlalchemy import and_, desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_test_user_if_not_exist(session_: AsyncSession):
    query = select(User).where(User.api_key == "test")
    user_query = await session_.execute(query)
    user = user_query.scalar_one_or_none()
    if user is None:
        user = User(api_key="test", username="test user")
        session_.add(user)
        await session_.commit()


async def get_user_by_api_key(
    api_key: str, session: AsyncSession = Depends(async_get_db)
):
    query = (
        select(User)
        .where(User.api_key == api_key)
        .options(
            selectinload(User.following),
            selectinload(User.followers),
        )
    )
    user = await session.execute(query)

    return user.scalar_one_or_none()


async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(async_get_db)
):
    query = await session.execute(
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.following),
            selectinload(User.followers),
        )
    )
    user = query.scalars().one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist.",
        )
    return user


async def check_follow_user_ability(
    current_user: User,
    user_being_followed: User,
) -> bool:
    """Check if the following requests matches all the criteria"""

    if user_being_followed.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to follow yourself",
        )

    elif user_being_followed in current_user.following:
        return False
    return True


async def associate_media_with_tweet(
    tweet: Tweet,
    media_ids: List[int],
    session: AsyncSession = Depends(async_get_db),
):
    """
    Associate one or more Media objects with a Tweet.

    Args:
        session (Session): The SQLAlchemy session.
        tweet (Tweet): The Tweet object to associate with Media.
        media_ids (List[int]): List of media IDs to associate with the Tweet.
    """
    media_query = await session.execute(
        select(Media).filter(Media.id.in_(media_ids))
    )

    media_objects = media_query.scalars()

    for media in media_objects:
        if not media.tweet_id:
            media.tweet_id = tweet.id

    session.add_all(media_objects)


async def get_media_by_tweet_id(
    tweet_id: int, session: AsyncSession = Depends(async_get_db)
):
    """
    Get all Media objects associate with Tweet.

    Args:
        session (Session): The SQLAlchemy session.
        tweet_id (int): The Tweet object id.
    """
    media_query = await session.execute(
        select(Media).filter(Media.tweet_id == tweet_id)
    )
    media_objects = media_query.scalars().all()
    return media_objects


async def get_tweet_by_id(
    tweet_id: int,
    session: AsyncSession = Depends(async_get_db),
):
    """
    Retrieve a tweet by its unique identifier.

    Parameters:
    - tweet_id (int): The unique identifier of the tweet to retrieve.
    - session (AsyncSession, optional): An SQLAlchemy async session
      (provided by `get_db_session`)
      used to interact with the database.

    Returns:
    - Tweet: The retrieved tweet object.

    Raises:
    - HTTPException: If the tweet with the specified `tweet_id` is not
      found in the database,
      an HTTPException with a status code of 404 (Not Found) is raised.
    """
    tweet = await session.get(Tweet, tweet_id)

    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet was not found!",
        )
    return tweet


async def get_all_following_tweets(session: AsyncSession, current_user: User):
    query = await session.execute(
        select(Tweet)
        .where(
            or_(
                Tweet.user_id.in_(uuid.id for uuid in current_user.following),
                Tweet.user_id == current_user.id,
            )
        )
        .options(
            selectinload(Tweet.user),
            selectinload(Tweet.likes),
            selectinload(Tweet.media),
        )
        .order_by(desc(Tweet.create_date))
    )

    return query.scalars().all()


async def get_all_tweets(session: AsyncSession):
    query = await session.execute(
        select(Tweet)
        .options(
            selectinload(Tweet.user),
            selectinload(Tweet.likes),
            selectinload(Tweet.media),
        )
        .order_by(desc(Tweet.create_date))
    )
    return query.scalars().all()


async def get_like_by_id(session: AsyncSession, tweet_id: int, user_id: int):
    """Get a like by user_id and tweet_id, or return None if not found"""
    query = await session.execute(
        select(Like).where(
            and_(Like.user_id == user_id, Like.tweet_id == tweet_id)
        )
    )
    return query.scalar_one_or_none()
