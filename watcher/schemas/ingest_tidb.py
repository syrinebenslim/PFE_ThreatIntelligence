import dataclasses

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, declarative_base


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

    def get_session(self):
        session = None
        Base = declarative_base()
        try:

            Base.metadata.create_all(self.engine)

            print(
                f"Connection to the {self.engine} for user {self.engine} created successfully.")
            Session = DatabaseConnection().get_sessions()
            session = Session()

        except Exception as ex:
            print("Connection/Session could not be made due to the following error: \n", ex)
        return session


@dataclasses.dataclass
class QueryShadowServerFeeds:

    def append_feeds(self, session, list_feeds):
        session.bulk_save_objects(list_feeds)
        session.commit()

    def append_feed(self, session, feed):
        session.add(feed)
        session.commit()

