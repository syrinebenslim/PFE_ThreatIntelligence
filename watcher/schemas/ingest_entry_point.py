# This is a sample Python script.


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from watcher.schemas.ingest_tidb import QueryPlayer, DatabaseConnection


def main():
    # Use a breakpoint in the code line below to debug your script.
    try:
        engine = DatabaseConnection().engine
        print(
            f"Connection to the {engine} for user {engine} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)


    QueryPlayer().simple_example()
    QueryPlayer().trade_example()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
