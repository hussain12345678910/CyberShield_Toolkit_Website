import os
import datetime


TOOL_CONFIG = {
    "name": "File Metadata Viewer",
    "slug": "meta",
    "description": "View detailed metadata of files including size, timestamps, and type.",
    "icon": "bi-info-circle",
    "button_text": "Get Metadata",
    "fields": [
        {
            "name": "file_path",
            "label": "File Path",
            "type": "text",
            "placeholder": "example.txt",
            "required": False
        },
        {
            "name": "file_list",
            "label": "Multiple Files (comma separated)",
            "type": "text",
            "placeholder": "file1.txt, file2.txt",
            "required": False
        }
    ],
    "result_columns": ["#", "File", "Details"]
}


class FileMetadataViewer:

    def get_metadata(self, file_path):

        if not os.path.exists(file_path):
            return None

        try:
            stat = os.stat(file_path)

            return {
                "name": os.path.basename(file_path),
                "path": os.path.abspath(file_path),
                "size": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.datetime.fromtimestamp(stat.st_atime),
                "is_file": os.path.isfile(file_path),
                "extension": os.path.splitext(file_path)[1]
            }

        except:
            return None


def run(data):

    viewer = FileMetadataViewer()

    file_path = data.get("file_path", "").strip()
    file_list = data.get("file_list", "").strip()

    rows = []

    # ----------------------------
    # SINGLE FILE MODE
    # ----------------------------
    if file_path:

        meta = viewer.get_metadata(file_path)

        if not meta:
            return {
                "success": False,
                "error": "File not found"
            }

        rows.append([
            1,
            meta["name"],
            f"Size: {meta['size_mb']} MB | "
            f"Type: {'File' if meta['is_file'] else 'Dir'} | "
            f"Modified: {meta['modified']}"
        ])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": "Single file metadata retrieved successfully"
        }

    # ----------------------------
    # BATCH MODE
    # ----------------------------
    if file_list:

        files = [f.strip() for f in file_list.split(",") if f.strip()]

        count = 1

        for f in files:
            meta = viewer.get_metadata(f)

            if meta:
                rows.append([
                    count,
                    meta["name"],
                    f"{meta['size_mb']} MB | {meta['extension']} | {meta['modified']}"
                ])
                count += 1

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"Processed {len(rows)} file(s)"
        }

    return {
        "success": False,
        "error": "No file path provided"
    }