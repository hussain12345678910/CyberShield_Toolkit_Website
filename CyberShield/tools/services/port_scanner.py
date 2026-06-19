import random

TOOL_CONFIG = {
    "name": "Port Scanner",
    "slug": "portscan",
    "description": "Simulated TCP port scanner for network analysis",
    "icon": "bi-search",
    "button_text": "Scan Ports",
    "fields": [
        {
            "name": "ip",
            "label": "Target IP Address",
            "type": "text",
            "placeholder": "e.g. 192.168.1.1",
            "required": True
        },
        {
            "name": "ports",
            "label": "Ports (comma separated)",
            "type": "text",
            "placeholder": "e.g. 22,80,443",
            "required": True
        }
    ],
    "result_columns": ["Port", "Service", "Status"]
}


COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB"
}


def scan_port(port):
    # simple simulation logic
    common_open = [80, 443, 22, 53]

    if port in common_open:
        status = "open" if random.random() > 0.3 else "closed"
    else:
        status = "filtered" if random.random() > 0.5 else "closed"

    return status


def run(data):
    ip = data.get("ip", "").strip()
    ports_input = data.get("ports", "")

    if not ip:
        return {
            "success": False,
            "error": "IP address is required"
        }

    try:
        ports = [int(p.strip()) for p in ports_input.split(",") if p.strip()]
    except:
        return {
            "success": False,
            "error": "Invalid ports format. Use comma separated numbers"
        }

    if not ports:
        return {
            "success": False,
            "error": "At least one port required"
        }

    rows = []

    for port in ports:
        service = COMMON_SERVICES.get(port, "Unknown")
        status = scan_port(port)

        rows.append([
            port,
            service,
            status.upper()
        ])

    return {
        "success": True,
        "columns": TOOL_CONFIG["result_columns"],
        "rows": rows,
        "summary": f"Scanned {len(ports)} ports on {ip}"
    }