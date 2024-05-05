import os
import threading
import time

import watchdog.events
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from watcher.event_handlers import ServerWorkSync
from watcher.feed_parsers_shadow import FeedParser

# Define the directory to monitor
directory_to_watch = '/home/zouaoui'


# Define a custom handler to handle file creation events
class FeedEventHandler(PatternMatchingEventHandler):

    def __init__(self, sftp_client, local_dir, remote_dir):
        watchdog.events.PatternMatchingEventHandler.__init__(patterns=["*.csv"],
                                                             ignore_patterns=[],
                                                             ignore_directories=True, case_sensitive=False)
        self.sftp_client = sftp_client
        self.local_dir = local_dir
        self.remote_dir = remote_dir
        super().__init__()

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            basename = os.path.basename(event.src_path)
            print(FeedParser(basename).parse_feed_name())

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)


# Create an observer to watch the directory

class FeedWatcher:

    def __init__(self, ssh_client, localpath, remotepath):
        self.ssh_client = ssh_client
        self.localpath = localpath
        self.remotepath = remotepath
        self.observer = Observer()

    def run(self):
        self.observer.schedule(
            ServerWorkSync(self.ssh_client, localpath=self.localpath, remotepath=self.remotepath,verbose=True),
            self.localpath, recursive=True)
        observer_thread = threading.Thread(target=self.observer.start)
        observer_thread.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Error")

        observer_thread.join()
