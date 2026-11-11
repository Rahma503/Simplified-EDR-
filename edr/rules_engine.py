import yaml, time
from collections import deque
from edr.logger import log_alert
from edr.response import kill_process, quarantine_file

class RulesEngine:
    def __init__(self, rules_path="rules/rules.yaml", auto_respond=False):
        with open(rules_path) as f:
            self.rules = yaml.safe_load(f)
        self.auto_respond = auto_respond
        self.recent_mods = deque()

    def alert(self, rule, severity, details, pid=None, path=None):
        log_alert({"rule": rule, "severity": severity, "details": details})
        if self.auto_respond:
            if pid: kill_process(pid)
            if path: quarantine_file(path)

    def handle(self, e):
        t = e["type"]
        if t == "process_start":   self.check_process(e)
        elif t == "file_created":  self.check_file(e)
        elif t == "file_modified": self.check_ransomware(e)
        elif t == "network_connection": self.check_network(e)

    def check_process(self, e):
        if e["name"] in self.rules["suspicious_process_names"]:
            self.alert("Known malicious tool", "high", e["name"], pid=e["pid"])
        for r in self.rules["suspicious_parent_child"]:
            if e["parent"] == r["parent"] and e["name"] == r["child"]:
                self.alert("Suspicious parent-child", "high",
                           f'{r["parent"]} -> {r["child"]}', pid=e["pid"])
        if any(p in e["exe"] for p in self.rules["suspicious_paths"]):
            self.alert("Process from suspicious path", "medium", e["exe"], pid=e["pid"])

    def check_file(self, e):
        if any(e["path"].endswith(x) for x in self.rules["monitored_extensions"]):
            self.alert("Executable file dropped", "medium", e["path"], path=None)

    def check_ransomware(self, e):
        cfg = self.rules["ransomware"]
        now = e["ts"]
        self.recent_mods.append(now)
        while self.recent_mods and now - self.recent_mods[0] > cfg["time_window_seconds"]:
            self.recent_mods.popleft()
        if len(self.recent_mods) >= cfg["files_modified_threshold"]:
            self.alert("Possible ransomware behavior", "critical",
                       f"{len(self.recent_mods)} files modified in {cfg['time_window_seconds']}s")
            self.recent_mods.clear()

    def check_network(self, e):
        if e["remote_port"] in self.rules["suspicious_ports"]:
            self.alert("Connection to suspicious port", "high",
                       f'{e["remote_ip"]}:{e["remote_port"]}', pid=e["pid"])