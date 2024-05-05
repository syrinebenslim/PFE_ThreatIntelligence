from sqlalchemy import Column, TIMESTAMP, JSON, VARBINARY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ShadowServerFeeds(Base):
    __abstract__ = True
    uuid = Column(VARBINARY(16), primary_key=True)
    payload = Column(JSON)
    ts = Column(TIMESTAMP)


class Event4MicrosoftSinkhole(ShadowServerFeeds):
    __tablename__ = "event4_microsoft_sinkhole "

    def __repr__(self):
        return f'Event4MicrosoftSinkhole(id={self.uuid!r}, payload={self.payload!r}, ts={self.ts!r})'
