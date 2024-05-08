import os
import threading
import time
import uuid

import watchdog.events
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from watcher.feed_parsers_shadow import FeedParser
# Define the directory to monitor
from watcher.parser.data_parser import Csv2Json
from watcher.schemas.ingest_tidb import DatabaseConnection, QueryShadowServerFeeds

directory_to_watch = '/home/zouaoui'


# Define a custom handler to handle file creation events
class FeedEventHandler(PatternMatchingEventHandler):

    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(patterns=["*.csv"],
                                                             ignore_patterns=[],
                                                             ignore_directories=True, case_sensitive=False)

        self.db_session = DatabaseConnection().get_session()
        super().__init__()

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            basename = os.path.basename(event.src_path)
            data, name = FeedParser(basename).parse_feed_name()
            print(name)

            if self.db_session is not None:

                jsons_data = Csv2Json(event.src_path) \
                    .make_json()
                json_list = []
                case_class = self.to_camel_case(name)
                print(f"CLASS  <{case_class}>")
                for data in jsons_data:
                    json_list.append(
                        globals()[case_class](uuid=uuid.uuid4().bytes, payload=data))

                QueryShadowServerFeeds().append_feeds(self.db_session, json_list)

            else:
                print("Session could not be made")

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)

    def to_camel_case(self, test_str):
        # printing original string
        print("The original string is : " + str(test_str))

        # split underscore using split
        temp = test_str.split('_')

        # joining result
        res = temp[0] + ''.join(ele.title() for ele in temp[1:])

        # printing result
        print("The camel case string is : " + str(res))

        return str(res).title()


# Create an observer to watch the directory

class FeedWatcher:

    def __init__(self, local_path):
        self.local_path = local_path
        self.observer = Observer()

    def run(self):
        self.observer.schedule(
            FeedEventHandler(),
            self.local_path, recursive=True)
        observer_thread = threading.Thread(target=self.observer.start)
        observer_thread.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Error")

        observer_thread.join()
