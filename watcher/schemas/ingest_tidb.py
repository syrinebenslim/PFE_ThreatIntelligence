import uuid
from typing import List

from sqlalchemy import create_engine, select, func
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from watcher.schemas.models import Player


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


class QueryPlayer:

    def random_player(self, amount: int) -> List[Player]:
        players = []
        for _ in range(amount):
            players.append(Player(id=uuid.uuid4(), coins=10000, goods=10000))

        return players

        import uuid

        def simple_example(self, session) -> None:
            # Vérifier si l'ID "test" existe déjà
            test_player = session.query(Player).filter_by(id="test").first()
            if test_player is None:
                # Si l'ID "test" n'existe pas, l'insérer
                session.add(Player(id="test", coins=1, goods=1))

            # get this player, and print it.
            get_test_stmt = select(Player).where(Player.id == "test")
            for player in session.scalars(get_test_stmt):
                print(player)

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = self.random_player(1919)
            for idx in range(0, len(player_list), 114):
                session.bulk_save_objects(player_list[idx:idx + 114])

            # print the number of players
            count = session.query(func.count(Player.id)).scalar()
            print(f'number of players: {count}')

            # print 3 players.
            three_players = session.query(Player).limit(3).all()
            for player in three_players:
                print(player)

            session.commit()

