import time
from collections import deque
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from edr.logger import log_event

class Handler(FileSystemEventHandler):
    def __init__(self, on_event):
        self.on_event = on_event

    def _emit(self, kind, path):
        event = {"type": kind, "path": path.lower(), "ts": time.time()}
        log_event(event)
        self.on_event(event)

    def on_created(self, e):
        if not e.is_directory: self._emit("file_created", e.src_path)

    def on_modified(self, e):
        if not e.is_directory: self._emit("file_modified", e.src_path)

def monitor_files(paths, on_event):
    observer = Observer()
    for p in paths:
        observer.schedule(Handler(on_event), p, recursive=True)
    observer.start()
    while True:
        time.sleep(1)