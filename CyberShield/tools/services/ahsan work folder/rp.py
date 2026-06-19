import random
import string

TOOL_CONFIG = {
    "name": "Random Password Generator",
    "description": "Generate secure random password",
    "fields": [
        {"name": "length", "placeholder": "Enter length"}
    ]
}

def random_password(data):
    length = int(data.get("length", 10))

    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(length))

    return {
        "success": True,
        "summary": "Password generated",
        "rows": [["Password", password]],
        "columns": ["Type", "Value"]
    }