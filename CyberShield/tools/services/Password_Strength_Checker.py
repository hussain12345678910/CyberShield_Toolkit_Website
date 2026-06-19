import re


TOOL_CONFIG = {
    "name": "Password Strength Checker",
       "slug": "password",
    "description": "Analyze password strength in real-time security rules",
    "icon": "bi-shield-lock",
    "button_text": "Check Password",
    "fields": [
        {
            "name": "password",
            "label": "Enter Password",
            "type": "password",
            "placeholder": "Type password here",
            "required": True
        }
    ],
    "result_columns": ["Rule", "Status"]
}


class PasswordAnalyzer:

    def analyse(self, pw):
        return {
            "length": len(pw),
            "upper": bool(re.search(r"[A-Z]", pw)),
            "lower": bool(re.search(r"[a-z]", pw)),
            "number": bool(re.search(r"[0-9]", pw)),
            "symbol": bool(re.search(r"[^A-Za-z0-9]", pw))
        }

    def score(self, a):
        return sum([
            a["upper"],
            a["lower"],
            a["number"],
            a["symbol"]
        ])


def run(data):

    pw = data.get("password", "").strip()

    if not pw:
        return {
            "success": False,
            "error": "Password is required"
        }

    analyzer = PasswordAnalyzer()
    a = analyzer.analyse(pw)
    score = analyzer.score(a)

    rows = []

    # ── RULE CHECKS ──
    rows.append(["Length >= 8", "PASS" if a["length"] >= 8 else "FAIL"])
    rows.append(["Uppercase Letter", "PASS" if a["upper"] else "FAIL"])
    rows.append(["Lowercase Letter", "PASS" if a["lower"] else "FAIL"])
    rows.append(["Number", "PASS" if a["number"] else "FAIL"])
    rows.append(["Symbol", "PASS" if a["symbol"] else "FAIL"])

    # ── STRENGTH LOGIC (same as JS) ──
    if a["length"] >= 8 and score == 4:
        strength = "STRONG PASSWORD"
    elif a["length"] >= 6 and score >= 2:
        strength = "MEDIUM PASSWORD"
    else:
        strength = "WEAK PASSWORD"

    return {
        "success": True,
        "columns": TOOL_CONFIG["result_columns"],
        "rows": rows,
        "summary": strength
    }