

import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from watcher.feed_parsers_shadow import FeedParser
from watchdog.events import PatternMatchingEventHandler
# Define the directory to monitor
directory_to_watch = '/data/vulnerabilities'


# Define a custom handler to handle file creation events
class FeedEventHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        print("bloc creation")
        try:
            if event.is_directory:
                print(f"Directory created: {event.src_path}")
            else:
                print(f"File created: {event.src_path}")
                basename = os.path.basename(event.src_path)
                print(FeedParser(basename).parse_feed_name())
        except Exception as e:
            print(f'Error in on_created event handler: {e}')

    def on_modified(self, event):
        try:
            print(f"File modified: {event.src_path}")
            print("bloc modification")

        except Exception as e:
            print(f'Error in on_created event handler: {e}')



# Create an observer to watch the directory

class FeedWatcher:
    print(directory_to_watch)
    print("new code")
    observer = Observer()
    observer.schedule(FeedEventHandler(patterns=["*.csv"],
                              ignore_patterns=[],
                              ignore_directories=True
                              ), directory_to_watch, recursive=True)

    # Start the observer
    observer.start()

    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        # Stop the observer if Ctrl+C is pressed
        observer.stop()

    # Wait for the observer's thread to finish
    observer.join()