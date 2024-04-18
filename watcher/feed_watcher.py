import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from watcher.feed_parsers_shadow import FeedParser

# Define the directory to monitor
directory_to_watch = '/data/vulnerabilities'


# Define a custom handler to handle file creation events
class FeedEventHandler(FileSystemEventHandler):
    def on_created(self, event):
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
            print(f"File created: {event.src_path}")

        except Exception as e:
            print(f'Error in on_created event handler: {e}')



# Create an observer to watch the directory

class FeedWatcher:
    print(directory_to_watch)
    observer = Observer()
    observer.schedule(FeedEventHandler(), directory_to_watch, recursive=True)

    # Start the observer
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer if Ctrl+C is pressed
        observer.stop()

    # Wait for the observer's thread to finish
    observer.join()
