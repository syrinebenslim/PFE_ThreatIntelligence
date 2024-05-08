# This is a sample Python script.
import uuid

from sqlalchemy.orm import declarative_base

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from watcher.parser.data_parser import Csv2Json
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds
from watcher.schemas.models import Event4MicrosoftSinkhole


def main():
    # Use a breakpoint in the code line below to debug your script.
    session = get_session()

    if session is not None:

        jsons_data = Csv2Json("/data/vulnerabilities/2022-09-19-event4_microsoft_sinkhole-tunisia-geo.csv").make_json()
        event4_microsoft_sinkhole_list = []
        for data in jsons_data:
            event4_microsoft_sinkhole_list.append(Event4MicrosoftSinkhole(uuid=uuid.uuid4().bytes, payload=data))

        QueryShadowServerFeeds().append_feeds(session, event4_microsoft_sinkhole_list)

    else:
        print("Session could not be made")


def get_session():
    session = None
    Base = declarative_base()
    try:
        engine = DatabaseConnection().engine

        Base.metadata.create_all(engine)

        print(
            f"Connection to the {engine} for user {engine} created successfully.")
        Session = DatabaseConnection().get_sessions()
        session = Session()

    except Exception as ex:
        print("Connection/Session could not be made due to the following error: \n", ex)
    return session


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
