import time

from paramiko import SSHClient
from watchdog.observers import Observer


class ServerError(Exception):
    pass


class Server(object):

    def __init__(self, event_handler):
        """
        See management command :func:`start_observer` or tests for usage.

        :param event_handler: an instance of :class:`BaseEventHandler`.
        """
        self.event_handler = event_handler

    def __str__(self):
        return 'Server started '

    def observe(self, sleep=None):
        with SSHClient() as self.event_handler.ssh:
            observer = Observer()
            observer.schedule(self.event_handler, path=self.event_handler.source_dir)
            self.event_handler.connect()
            self.event_handler.process_existing_files()
            observer.start()
            try:
                while True:
                    time.sleep(sleep or 1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
