import psutil, time
from edr.logger import log_event

def monitor_network(on_event, interval=2):
    seen = set()
    while True:
        for c in psutil.net_connections(kind="inet"):
            if c.status == "ESTABLISHED" and c.raddr:
                key = (c.pid, c.raddr.ip, c.raddr.port)
                if key not in seen:
                    seen.add(key)
                    event = {"type": "network_connection", "pid": c.pid,
                             "remote_ip": c.raddr.ip, "remote_port": c.raddr.port}
                    log_event(event)
                    on_event(event)
        time.sleep(interval)