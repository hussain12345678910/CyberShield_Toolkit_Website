import requests
from urllib.parse import urlparse

TOOL_CONFIG = {
    "name": "URL Safety Checker",
    "slug": "url",
    "description": "Analyze URLs for phishing patterns, HTTPS, domain structure, and reachability.",
    "icon": "bi-shield-check",
    "button_text": "Check URL",
    "fields": [
        {
            "name": "url",
            "label": "URL to Check",
            "type": "text",
            "placeholder": "https://example.com",
            "required": True
        }
    ],
    "result_columns": ["Check", "Result"]
}


def run(data):
    url = data.get("url", "").strip()
    if not url:
        return {"success": False, "error": "URL is required"}
    if not url.startswith("http"):
        url = "http://" + url
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        rows = []

        # HTTPS check
        if url.startswith("https://"):
            rows.append(["HTTPS Enabled", "✔ Secure"])
        else:
            rows.append(["HTTPS Enabled", "⚠ Not Secure"])

        # Domain structure
        if domain.count(".") > 2:
            rows.append(["Domain Structure", "⚠ Suspicious subdomains"])
        else:
            rows.append(["Domain Structure", "✔ Normal"])

        # Keyword check
        suspicious_words = ["login", "verify", "update", "bank", "free", "secure"]
        found = [w for w in suspicious_words if w in url.lower()]
        if found:
            rows.append(["Phishing Keywords", f"⚠ Found: {', '.join(found)}"])
        else:
            rows.append(["Phishing Keywords", "✔ None detected"])

        # Reachability
        try:
            resp = requests.get(url, timeout=5)
            rows.append(["Reachability", f"✔ Online (HTTP {resp.status_code})"])
        except Exception:
            rows.append(["Reachability", "❌ Not reachable"])

        risk = sum(1 for r in rows if "⚠" in r[1] or "❌" in r[1])
        summary = f"Risk level: {'HIGH' if risk >= 3 else 'MEDIUM' if risk >= 1 else 'LOW'} — {risk} warning(s) found"

        return {
            "success": True,
            "url": url,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": summary
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
