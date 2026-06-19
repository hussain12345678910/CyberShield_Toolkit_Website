import random
import string

TOOL_CONFIG = {
    "name": "Random Password Generator",
    "slug": "random",
    "description": "Generate strong random passwords with custom options.",
    "icon": "bi-shield-lock",
    "button_text": "Generate Passwords",
    "fields": [
        {
            "name": "length",
            "label": "Password Length",
            "type": "number",
            "placeholder": "Enter length (8-32)",
            "required": True
        },
        {
        "name": "uppercase",
        "label": "Include Uppercase",
        "type": "select",
        "options": [
            {"label": "True", "value": "true"},
            {"label": "False", "value": "false"}    
        ]
    },
    {
        "name": "lowercase",
        "label": "Include Lowercase",
        "type": "select",
        "options": [
            {"label": "True", "value": "true"},
            {"label": "False", "value": "false"}
        ]
    },
    {
        "name": "numbers",
        "label": "Include Numbers",
        "type": "select",
        "options": [
            {"label": "True", "value": "true"},
            {"label": "False", "value": "false"}
        ]
    },
    {
        "name": "symbols",
        "label": "Include Symbols",
        "type": "select",
        "options": [
            {"label": "True", "value": "true"},
            {"label": "False", "value": "false"}
        ]
    }
    ],
    "result_columns": ["#", "Password"]
}


# ─────────────────────────────────────────────
# CORE LOGIC (same as your JS)
# ─────────────────────────────────────────────

def build_charset(flags):
    chars = ""

    if flags.get("uppercase") == "true":
        chars += string.ascii_uppercase

    if flags.get("lowercase") == "true":
        chars += string.ascii_lowercase

    if flags.get("numbers") == "true":
        chars += string.digits

    if flags.get("symbols") == "true":
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    return chars


def generate_password(length, charset):
    return "".join(random.choice(charset) for _ in range(length))


def run(data):
    try:
        length = int(data.get("length", 12))
        count = int(data.get("count", 4))

        flags = {
            "uppercase": data.get("uppercase", "true"),
            "lowercase": data.get("lowercase", "true"),
            "numbers": data.get("numbers", "true"),
            "symbols": data.get("symbols", "true"),
        }

        charset = build_charset(flags)

        if not charset:
            return {
                "success": False,
                "error": "Select at least one character type"
            }

        rows = []

        for i in range(count):
            pw = generate_password(length, charset)
            rows.append([i + 1, pw])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"{count} passwords generated successfully (Length: {length})"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }