from typing import Annotated, Union

from aiofiles import os as aiofiles_os
from database.database import async_get_db
from database.utils import (
    associate_media_with_tweet,
    get_all_following_tweets,
    get_all_tweets,
    get_like_by_id,
    get_media_by_tweet_id,
    get_tweet_by_id,
    get_user_by_id,
)
from fastapi import APIRouter, Depends, HTTPException, status
from models.likes import Like
from models.tweets import Tweet
from models.users import User
from schemas.base_schema import DefaultSchema
from schemas.tweet_schema import TweetCreate, TweetIn, TweetOut
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from utils.auth import authenticate_user
from utils.settings import MEDIA_PATH

router = APIRouter(prefix="/api", tags=["tweets_and_likes_v1"])


@router.post(
    "/tweets",
    status_code=status.HTTP_201_CREATED,
    response_model=Union[TweetIn, TweetCreate],
)
async def create_tweet(
    tweet_in: TweetIn,
    current_user: Annotated[
        User, "User model obtained from the api key"
    ] = Depends(authenticate_user),
    session: AsyncSession = Depends(async_get_db),
):
    new_tweet = Tweet(
        user_id=current_user.id,
        tweet_data=tweet_in.tweet_data,
    )
    session.add(new_tweet)
    await session.flush()
    tweet_media_ids = tweet_in.tweet_media_ids

    if tweet_media_ids:
        await associate_media_with_tweet(
            session=session, media_ids=tweet_media_ids, tweet=new_tweet
        )

    await session.commit()

    return {"result": True, "tweet_id": new_tweet.id}


@router.delete(
    "/tweets/{tweet_id}",
    status_code=status.HTTP_200_OK,
    response_model=DefaultSchema,
)
async def delete_tweet(
    tweet_id: int,
    current_user: Annotated[
        User, "User model obtained from the api key"
    ] = Depends(authenticate_user),
    session: AsyncSession = Depends(async_get_db),
):
    tweet_to_delete = await get_tweet_by_id(tweet_id, session)
    if tweet_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sorry, you can't delete tweets created by another user.",
        )
    media_to_delete = await get_media_by_tweet_id(tweet_id, session)
    for media in media_to_delete:
        path_to_delete = MEDIA_PATH / media.media_path
        await aiofiles_os.remove(path_to_delete)

    await session.delete(tweet_to_delete)
    await session.commit()
    return tweet_to_delete


@router.post(
    "/tweets/{tweet_id}/likes",
    status_code=status.HTTP_201_CREATED,
    response_model=DefaultSchema,
)
async def like_a_tweet(
    tweet_id: int,
    current_user: Annotated[
        User, "User model obtained from the api key"
    ] = Depends(authenticate_user),
    session: AsyncSession = Depends(async_get_db),
):
    tweet_to_like = await get_tweet_by_id(tweet_id=tweet_id, session=session)
    like = await get_like_by_id(
        session=session, tweet_id=tweet_id, user_id=current_user.id
    )
    if not like:
        if tweet_to_like.user_id != current_user.id:
            like_to_add = Like(
                user_id=current_user.id, tweet_id=tweet_to_like.id
            )
            session.add(like_to_add)
            await session.commit()

    return dict()


@router.delete(
    "/tweets/{tweet_id}/likes",
    status_code=status.HTTP_200_OK,
    response_model=DefaultSchema,
)
async def delete_like_from_tweet(
    tweet_id: int,
    current_user: Annotated[
        User, "User model obtained from the api key"
    ] = Depends(authenticate_user),
    session: AsyncSession = Depends(async_get_db),
):
    await session.commit()
    test_tweet = await get_tweet_by_id(tweet_id=tweet_id, session=session)
    like = await get_like_by_id(
        session, tweet_id=test_tweet.id, user_id=current_user.id
    )
    if like:
        await session.delete(like)
        await session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You already do not like that tweet.",
        )

    return dict()


@router.get("/tweets", status_code=status.HTTP_200_OK)
async def get_tweets(
    current_user: Annotated[
        User, "User model obtained from the api key"
    ] = Depends(authenticate_user),
    session: AsyncSession = Depends(async_get_db),
):
    all_tweets = await get_all_tweets(session=session)
    all_following_tweets = []
    if all_tweets is None:
        all_tweets = "No tweets found"
    else:
        for tweet in all_tweets:
            single_tweet = dict()
            single_tweet["id"] = tweet.id
            single_tweet["content"] = tweet.tweet_data
            single_tweet_media = []
            for media in tweet.media:
                single_tweet_media.append(media.media_path)
            single_tweet["attachments"] = single_tweet_media
            single_tweet_author = dict()

            single_tweet_author["id"] = tweet.user_id
            tweet_author = await get_user_by_id(tweet.user_id, session)
            single_tweet_author["name"] = tweet_author.username
            single_tweet["author"] = single_tweet_author

            single_tweet_likes = []
            for like in tweet.likes:
                single_like = dict()
                single_like["user_id"] = like.user_id
                tweet_author = await get_user_by_id(like.user_id, session)
                single_like["name"] = tweet_author.username
                single_tweet_likes.append(single_like)
            single_tweet["likes"] = single_tweet_likes

            all_following_tweets.append(single_tweet)
        all_tweets = all_following_tweets
    answer = dict()
    answer["result"] = True
    answer["tweets"] = all_tweets
    return JSONResponse(content=answer, status_code=200)


@router.get(
    "/tweets/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=TweetOut,
)
async def get_following_tweets(
    user_id: int,
    current_user: Annotated[
        User, "User model obtained from the api key"
    ] = Depends(authenticate_user),
    session: AsyncSession = Depends(async_get_db),
):
    all_tweets = await get_all_following_tweets(
        session=session, current_user=user_id
    )

    return {"tweets": all_tweets}
