import whois

TOOL_CONFIG = {
    "name": "WHOIS Lookup",
    "slug": "wis",
    "description": "Retrieve domain registration details, registrar info, and name servers.",
    "icon": "bi-search",
    "button_text": "Run WHOIS",
    "fields": [
        {
            "name": "domain",
            "label": "Domain Name",
            "type": "text",
            "placeholder": "example.com",
            "required": True
        }
    ],
    "result_columns": ["Field", "Value"]
}


def clean_domain(domain):
    domain = domain.strip().lower()
    domain = domain.replace("https://", "").replace("http://", "").replace("www.", "")
    domain = domain.split("/")[0]
    if "." not in domain:
        domain += ".com"
    return domain


def run(data):
    domain = clean_domain(data.get("domain", ""))
    if not domain:
        return {"success": False, "error": "Domain is required"}
    try:
        w = whois.whois(domain)
        rows = [
            ["Registrar", str(w.registrar or "N/A")],
            ["Creation Date", str(w.creation_date or "N/A")],
            ["Expiration Date", str(w.expiration_date or "N/A")],
            ["Country", str(w.country or "N/A")],
            ["Name Servers", str(w.name_servers or "N/A")],
        ]
        return {
            "success": True,
            "domain": domain,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"WHOIS data retrieved for {domain}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
