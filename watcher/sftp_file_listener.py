import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the directory to monitor
directory_to_watch = 'C:\\Users\\syrin\\Documents\\vilnera'

# Define a custom handler to handle file creation events
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"Directory created: {event.src_path}")
        else:
            print(f"File created: {event.src_path}")

# Create an observer to watch the directory
observer = Observer()
observer.schedule(MyHandler(), directory_to_watch, recursive=True)

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
