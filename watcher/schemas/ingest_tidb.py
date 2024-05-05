import dataclasses

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


class DatabaseConnection:
    def __init__(self):
        self.engine = self._get_db_engine()

    def _get_db_engine(self):
        return create_engine(
            URL.create(
                drivername="mysql+pymysql",
                username="root",
                password="changeit",
                host="192.168.1.140",
                port=4000,
                database="THREAT_INTELLIGENCE_FEEDS",
            ),
            connect_args={},
        )

    def get_sessions(self):
        return sessionmaker(bind=self.engine)


@dataclasses.dataclass
class QueryShadowServerFeeds:

    def append_feeds(self, session, list_feeds):
        session.bulk_save_objects(list_feeds)
        session.commit()

    def append_feed(self, session, feed):
        session.add(feed)
        session.commit()
