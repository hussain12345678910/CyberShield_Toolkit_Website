import hashlib

TOOL_CONFIG = {
    "name": "Hash Generator",
    "description": "Generate MD5 / SHA256 hash",
    "fields": [
        {"name": "text", "placeholder": "Enter text"},
        {"name": "type", "placeholder": "md5 or sha256"}
    ]
}

def make_hash(data):
    text = data.get("text", "")
    type_ = data.get("type", "sha256")

    if type_ == "md5":
        result = hashlib.md5(text.encode()).hexdigest()
    else:
        result = hashlib.sha256(text.encode()).hexdigest()

    return {
        "success": True,
        "summary": "Hash generated",
        "rows": [["Hash", result]],
        "columns": ["Type", "Value"]
    }