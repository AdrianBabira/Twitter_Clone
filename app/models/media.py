from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Media(Base):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )

    media_path: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id"), nullable=True
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            media_path=self.media_path,
            tweet_id=self.tweet_id,
        )
