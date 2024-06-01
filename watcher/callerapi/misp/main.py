from watcher.callerapi.misp.reader import MispReader


def main():
    # Use a breakpoint in the code line below to debug your script.

    w = MispReader("https://www.botvrij.eu/data/feed-osint")
    df = w.write_misp_events()
    if df is not None:
        print(df.info())
    else:
        print("DataFrame is None")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
