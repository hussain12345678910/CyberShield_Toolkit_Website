import hashlib


TOOL_CONFIG = {
    "name": "Hash Generator",
    "slug": "hash",
    "description": "Generate MD5 and SHA256 hashes from input text",
    "icon": "bi-hash",
    "button_text": "Generate Hash",
    "fields": [
        {
            "name": "text",
            "label": "Input Text",
            "type": "textarea",
            "placeholder": "Enter text to hash",
            "required": True
        },
        {
            "name": "type",
            "label": "Hash Type",
            "type": "select",
            "options": [
                {"label": "MD5", "value": "md5"},
                {"label": "SHA-256", "value": "sha256"},
                {"label": "Both", "value": "both"}
            ],
            "required": True
        }
    ],
    "result_columns": ["Type", "Value"]
}


class HashGenerator:

    def md5(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def sha256(self, text):
        return hashlib.sha256(text.encode()).hexdigest()


def run(data):

    text = data.get("text", "").strip()
    hash_type = data.get("type", "md5")

    if not text:
        return {
            "success": False,
            "error": "Text is required"
        }

    generator = HashGenerator()

    rows = []

    if hash_type == "md5":
        rows.append(["MD5", generator.md5(text)])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": "MD5 hash generated successfully"
        }

    elif hash_type == "sha256":
        rows.append(["SHA-256", generator.sha256(text)])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": "SHA-256 hash generated successfully"
        }

    else:  # both
        rows.append(["MD5", generator.md5(text)])
        rows.append(["SHA-256", generator.sha256(text)])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": "Both hashes generated successfully"
        }