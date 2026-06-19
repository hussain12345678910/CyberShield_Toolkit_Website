import os
import re
from collections import defaultdict

TOOL_CONFIG = {
    "name": "Log Analyzer",
    "slug": "log",
    "description": "Analyze log files for failed logins, errors, and suspicious IP activity.",
    "icon": "bi-file-earmark-text",
    "button_text": "Analyze Logs",
    "fields": [
        {
            "name": "log_file",
            "label": "Log File Path",
            "type": "text",
            "placeholder": "access.log",
            "required": True
        }
    ],
    "result_columns": ["#", "Category", "Detail"]
}


class LogAnalyzer:

    def __init__(self):
        self.log_entries = []

    def load_log(self, log_file):
        if not os.path.exists(log_file):
            return False, "File not found"

        self.log_entries = []

        try:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    self.log_entries.append({
                        "line_num": line_num,
                        "content": line.strip()
                    })
            return True, len(self.log_entries)

        except Exception as e:
            return False, str(e)

    def analyze_failed_logins(self):
        patterns = ["failed", "invalid", "incorrect", "authentication failed", "login failed"]
        results = []

        for entry in self.log_entries:
            for p in patterns:
                if p in entry["content"].lower():
                    results.append((entry["line_num"], entry["content"]))
                    break

        return results

    def analyze_errors(self):
        results = []
        for entry in self.log_entries:
            if "error" in entry["content"].lower() or "fail" in entry["content"].lower():
                results.append((entry["line_num"], entry["content"]))
        return results

    def analyze_ips(self):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        suspicious = []

        for entry in self.log_entries:
            ips = re.findall(ip_pattern, entry["content"])

            for ip in ips:
                if not (
                    ip.startswith("127.") or
                    ip.startswith("192.168.") or
                    ip.startswith("10.")
                ):
                    suspicious.append((ip, entry["line_num"], entry["content"]))

        return list(set(suspicious))


def run(data):

    log_file = data.get("log_file", "").strip()

    analyzer = LogAnalyzer()

    ok, msg = analyzer.load_log(log_file)

    if not ok:
        return {
            "success": False,
            "error": msg
        }

    rows = []

    # Failed logins
    failed = analyzer.analyze_failed_logins()
    for line, content in failed[:10]:
        rows.append([len(rows)+1, "FAILED LOGIN", f"Line {line}: {content[:60]}"])

    # Errors
    errors = analyzer.analyze_errors()
    for line, content in errors[:10]:
        rows.append([len(rows)+1, "ERROR", f"Line {line}: {content[:60]}"])

    # Suspicious IPs
    ips = analyzer.analyze_ips()
    for ip, line, content in ips[:10]:
        rows.append([len(rows)+1, "SUSPICIOUS IP", f"{ip} (Line {line})"])

    return {
        "success": True,
        "columns": TOOL_CONFIG["result_columns"],
        "rows": rows,
        "summary": (
            f"Log Entries: {msg} | "
            f"Failed: {len(failed)} | "
            f"Errors: {len(errors)} | "
            f"Suspicious IPs: {len(ips)}"
        )
    }