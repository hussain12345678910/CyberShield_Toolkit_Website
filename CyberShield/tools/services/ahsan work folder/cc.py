TOOL_CONFIG = {
    "name": "Caesar Cipher",
    "description": "Encrypt / Decrypt text using shift",
    "fields": [
        {"name": "text", "placeholder": "Enter text"},
        {"name": "shift", "placeholder": "Enter shift number"}
    ]
}

def caesar(data):
    text = data.get("text", "")
    shift = int(data.get("shift", 0))

    result = ""

    for i in text:
        if i.isalpha():
            base = 65 if i.isupper() else 97
            result += chr((ord(i) - base + shift) % 26 + base)
        else:
            result += i

    return {
        "success": True,
        "summary": "Cipher executed successfully",
        "rows": [["Result", result]],
        "columns": ["Type", "Value"]
    }