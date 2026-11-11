import threading, argparse
from edr.process_monitor import monitor_processes
from edr.file_monitor import monitor_files
from edr.network_monitor import monitor_network
from edr.rules_engine import RulesEngine

parser = argparse.ArgumentParser()
parser.add_argument("--watch", nargs="+", default=["./test_folder"])
parser.add_argument("--respond", action="store_true", help="enable auto response")
args = parser.parse_args()

engine = RulesEngine(auto_respond=args.respond)

threads = [
    threading.Thread(target=monitor_processes, args=(engine.handle,), daemon=True),
    threading.Thread(target=monitor_files, args=(args.watch, engine.handle), daemon=True),
    threading.Thread(target=monitor_network, args=(engine.handle,), daemon=True),
]
for t in threads: t.start()

print("EDR running... Ctrl+C to stop")
try:
    while True:
        threading.Event().wait(1)
except KeyboardInterrupt:
    print("Stopped.")