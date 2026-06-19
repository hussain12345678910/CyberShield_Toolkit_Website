TOOL_CONFIG = {
    "name": "Caesar Cipher",
    "slug": "caesar",
    "description": "Encrypt and Decrypt text using Caesar Cipher shift",
    "icon": "bi-shield-lock",
    "button_text": "Run Cipher",
    "fields": [
        {
            "name": "text",
            "label": "Input Text",
            "type": "textarea",
            "placeholder": "Enter text to encrypt or decrypt",
            "required": True
        },
        {
            "name": "shift",
            "label": "Shift Value",
            "type": "number",
            "placeholder": "Enter shift (1-25)",
            "required": True
        },
        {
            "name": "mode",
            "label": "Mode",
            "type": "select",
            "options": [
                {"label": "Encrypt", "value": "encrypt"},
                {"label": "Decrypt", "value": "decrypt"}
            ],
            "required": True
        }
    ],
    "result_columns": ["Type", "Value"]
}


class CaesarCipher:

    def __init__(self):
        pass

    def process(self, text, shift, mode):
        result = ""

        # normalize shift
        shift = int(shift) % 26

        # decrypt logic (same as your JS)
        if mode == "decrypt":
            shift = 26 - shift

        for ch in text:
            if ch.isalpha():
                base = 65 if ch.isupper() else 97
                result += chr(((ord(ch) - base + shift) % 26) + base)
            else:
                result += ch

        return result


def run(data):

    text = data.get("text", "").strip()
    shift = data.get("shift", 0)
    mode = data.get("mode", "encrypt")

    # validation
    if not text:
        return {
            "success": False,
            "error": "Text is required"
        }

    try:
        shift = int(shift)
    except:
        return {
            "success": False,
            "error": "Shift must be a valid number"
        }

    if mode not in ["encrypt", "decrypt"]:
        return {
            "success": False,
            "error": "Mode must be encrypt or decrypt"
        }

    cipher = CaesarCipher()
    result = cipher.process(text, shift, mode)

    return {
        "success": True,
        "columns": TOOL_CONFIG["result_columns"],
        "rows": [
            ["Mode", mode],
            ["Shift", shift],
            ["Input", text],
            ["Output", result]
        ],
        "summary": f"Caesar Cipher {mode} completed successfully"
    }