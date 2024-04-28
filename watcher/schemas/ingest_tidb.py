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
                username="threat_app_user",
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

    def simple_example(self) -> None:
        with DatabaseConnection().get_sessions() as session:
            # create a player, who has a coin and a goods.
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

    def trade_check(self, session, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
        # sell player goods check
        sell_player = session.query(Player.goods).filter(Player.id == sell_id).with_for_update().one()
        if sell_player.goods < amount:
            print(f'sell player {sell_id} goods not enough')
            return False

        # buy player coins check
        buy_player = session.query(Player.coins).filter(Player.id == buy_id).with_for_update().one()
        if buy_player.coins < price:
            print(f'buy player {buy_id} coins not enough')
            return False

    def trade(self, sell_id: str, buy_id: str, amount: int, price: int) -> None:
        with DatabaseConnection().get_sessions() as session:
            if self.trade_check(session, sell_id, buy_id, amount, price) is False:
                return

            # deduct the goods of seller, and raise his/her the coins
            session.query(Player).filter(Player.id == sell_id). \
                update({'goods': Player.goods - amount, 'coins': Player.coins + price})
            # deduct the coins of buyer, and raise his/her the goods
            session.query(Player).filter(Player.id == buy_id). \
                update({'goods': Player.goods + amount, 'coins': Player.coins - price})

            session.commit()
            print("trade success")

    def trade_example(self) -> None:
        with DatabaseConnection().get_sessions() as session:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            session.add(Player(id="1", coins=100, goods=0))
            session.add(Player(id="2", coins=114514, goods=20))
            session.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        self.trade(sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        self.trade(sell_id="2", buy_id="1", amount=2, price=100)

        with DatabaseConnection().get_sessions() as session:
            traders = session.query(Player).filter(Player.id.in_(("1", "2"))).all()
            for player in traders:
                print(player)
            session.commit()
