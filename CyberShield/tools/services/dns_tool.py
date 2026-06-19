import dns.resolver

TOOL_CONFIG = {
    "name": "DNS Lookup",
    "slug": "dns",
    "description": "Resolve domain names to IP addresses using real-time DNS queries.",
    "icon": "bi-globe",
    "button_text": "Run Lookup",
    "fields": [
        {
            "name": "domain",
            "label": "Domain Name",
            "type": "text",
            "placeholder": "example.com",
            "required": True
        }
    ],
    "result_columns": ["#", "IP Address"]
}


def clean_domain(domain):
    print(domain)
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
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8", "1.1.1.1"]
        resolver.timeout = 3
        resolver.lifetime = 3
        answers = resolver.resolve(domain, "A")
        rows = [[i, str(ip)] for i, ip in enumerate(answers, 1)]
        return {
            "success": True,
            "domain": domain,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"Found {len(rows)} IP address(es) for {domain}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
