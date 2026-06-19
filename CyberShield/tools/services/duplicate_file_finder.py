import os
import hashlib
from collections import defaultdict


TOOL_CONFIG = {
    "name": "Duplicate File Finder",
    "slug": "dup",
    "description": "Find duplicate files in a directory using SHA256 hashing.",
    "icon": "bi-files",
    "button_text": "Scan Duplicates",
    "fields": [
        {
            "name": "directory",
            "label": "Directory Path",
            "type": "text",
            "placeholder": "/home/user/downloads",
            "required": True
        }
    ],
    "result_columns": ["#", "File Group", "Details"]
}


class DuplicateFileFinder:

    def __init__(self):
        self.file_hashes = defaultdict(list)

    def calculate_hash(self, file_path):
        try:
            hasher = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return None

    def scan_directory(self, directory):
        if not os.path.exists(directory):
            return []

        files = []
        for root, _, filenames in os.walk(directory):
            for name in filenames:
                files.append(os.path.join(root, name))

        return files

    def find_duplicates(self, directory):

        files = self.scan_directory(directory)

        self.file_hashes = defaultdict(list)

        for f in files:
            file_hash = self.calculate_hash(f)
            if file_hash:
                self.file_hashes[file_hash].append(f)

        duplicates = {
            h: files for h, files in self.file_hashes.items()
            if len(files) > 1
        }

        return duplicates


def run(data):

    directory = data.get("directory", "").strip()

    finder = DuplicateFileFinder()

    if not os.path.exists(directory):
        return {
            "success": False,
            "error": "Directory not found"
        }

    duplicates = finder.find_duplicates(directory)

    rows = []

    if not duplicates:
        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": [],
            "summary": "No duplicate files found"
        }

    group_id = 1
    total_duplicates = 0
    wasted_space = 0

    for file_hash, files in duplicates.items():

        group_label = f"Group {group_id}"

        for f in files:
            size = os.path.getsize(f)
            wasted_space += size

            rows.append([
                group_id,
                group_label,
                f"{f} ({round(size / 1024, 2)} KB)"
            ])

        total_duplicates += len(files) - 1
        group_id += 1

    return {
        "success": True,
        "columns": TOOL_CONFIG["result_columns"],
        "rows": rows,
        "summary": (
            f"Duplicate Groups: {len(duplicates)} | "
            f"Duplicate Files: {total_duplicates} | "
            f"Wasted Space: {round(wasted_space / (1024*1024), 2)} MB"
        )
    }