import psutil, time
from edr.logger import log_event

def monitor_processes(on_event, interval=1):
    seen = set(psutil.pids())
    while True:
        current = set(psutil.pids())
        for pid in current - seen:
            try:
                p = psutil.Process(pid)
                parent = p.parent()
                event = {
                    "type": "process_start",
                    "pid": pid,
                    "name": p.name().lower(),
                    "exe": (p.exe() or "").lower(),
                    "cmdline": " ".join(p.cmdline()),
                    "parent": parent.name().lower() if parent else None,
                }
                log_event(event)
                on_event(event)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        seen = current
        time.sleep(interval)