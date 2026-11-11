import json, os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

def _write(path, data):
    data["timestamp"] = datetime.now().isoformat()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

def log_event(event):
    _write("logs/events.jsonl", event)

def log_alert(alert):
    _write("logs/alerts.jsonl", alert)
    print(f"[ALERT] {alert['rule']} | severity={alert['severity']} | {alert.get('details','')}")