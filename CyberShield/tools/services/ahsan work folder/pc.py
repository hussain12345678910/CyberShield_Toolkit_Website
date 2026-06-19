import string

TOOL_CONFIG = {
    "name": "Password Checker",
    "description": "Check password strength",
    "fields": [
        {"name": "password", "placeholder": "Enter password"}
    ]
}

def check_password(data):
    password = data.get("password", "")

    length = len(password)
    has_upper = any(i.isupper() for i in password)
    has_lower = any(i.islower() for i in password)
    has_number = any(i.isdigit() for i in password)
    has_symbol = any(i in string.punctuation for i in password)

    score = sum([has_upper, has_lower, has_number, has_symbol])

    if length >= 8 and score == 4:
        result = "Strong Password 👍"
    elif length >= 6 and score >= 2:
        result = "Medium Password 🙂"
    else:
        result = "Weak Password ⚠"

    return {
        "success": True,
        "summary": result,
        "rows": [],
        "columns": []
    }