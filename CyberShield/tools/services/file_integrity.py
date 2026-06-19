import hashlib
import os
import json
import datetime

TOOL_CONFIG = {
    "name": "File Integrity Checker",
    "slug": "file_integrity",
    "description": "Checks file integrity using cryptographic hashing (MD5, SHA1, SHA256, SHA512).",
    "icon": "bi-shield-lock",
    "button_text": "Check Integrity",
    "fields": [
        {
            "name": "files",
            "label": "File Paths (comma separated)",
            "type": "text",
            "placeholder": "file1.txt, file2.txt",
            "required": True
        },
        {
            "name": "algorithm",
            "label": "Hash Algorithm",
            "type": "select",
            "options": ["md5", "sha1", "sha256", "sha512"],
            "required": False
        }
    ],
    "result_columns": ["#", "File", "Status"]
}


class FileIntegrityChecker:
    def __init__(self):
        self.supported_algorithms = ["md5", "sha1", "sha256", "sha512"]

    def calculate_hash(self, file_path, algorithm="sha256"):
        if algorithm.lower() not in self.supported_algorithms:
            return None

        if not os.path.exists(file_path):
            return None

        try:
            if algorithm.lower() == "md5":
                hasher = hashlib.md5()
            elif algorithm.lower() == "sha1":
                hasher = hashlib.sha1()
            elif algorithm.lower() == "sha256":
                hasher = hashlib.sha256()
            elif algorithm.lower() == "sha512":
                hasher = hashlib.sha512()

            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)

            return hasher.hexdigest()

        except Exception:
            return None


def run(data):
    files = data.get("files", "")
    algorithm = data.get("algorithm", "sha256")

    file_list = [f.strip() for f in files.split(",") if f.strip()]

    checker = FileIntegrityChecker()

    rows = []
    results = {
        "total": len(file_list),
        "ok": 0,
        "missing": 0,
        "error": 0
    }

    for i, file_path in enumerate(file_list, 1):

        if not os.path.exists(file_path):
            rows.append([i, file_path, "MISSING"])
            results["missing"] += 1
            continue

        file_hash = checker.calculate_hash(file_path, algorithm)

        if file_hash:
            rows.append([i, file_path, "OK"])
            results["ok"] += 1
        else:
            rows.append([i, file_path, "ERROR"])
            results["error"] += 1

    return {
        "success": True,
        "columns": TOOL_CONFIG["result_columns"],
        "rows": rows,
        "summary": (
            f"Total: {results['total']} | "
            f"OK: {results['ok']} | "
            f"Missing: {results['missing']} | "
            f"Error: {results['error']}"
        )
    }