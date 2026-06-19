import random
import time
import socket

TOOL_CONFIG = {
    "name": "Ping Tester",
    "slug": "ping",
    "description": "ICMP-style ping simulation for host reachability check",
    "icon": "bi-wifi",
    "button_text": "Ping Host",
    "fields": [
        {
            "name": "host",
            "label": "Target IP / Hostname",
            "type": "text",
            "placeholder": "e.g. 8.8.8.8 or google.com",
            "required": True
        },
        {
            "name": "count",
            "label": "Number of Pings",
            "type": "number",
            "placeholder": "e.g. 8",
            "required": True
        }
    ],
    "result_columns": ["#", "Reply", "Time (ms)", "TTL"]
}


def is_reachable(host):
    """
    Lightweight reachability check (DNS + probabilistic simulation)
    """
    try:
        socket.gethostbyname(host)
        return True
    except Exception:
        return False


def simulate_ping(host):
    """
    Simulates latency like ICMP response
    """
    base = random.uniform(8, 60)
    jitter = random.uniform(0, 20)
    return round(base + jitter, 2)


def run(data):
    host = data.get("host", "").strip()
    count = int(data.get("count", 8))

    if not host:
        return {
            "success": False,
            "error": "Host is required"
        }

    reachable = is_reachable(host)

    # known stable hosts (just like your JS logic)
    known_hosts = ["8.8.8.8", "1.1.1.1", "google.com", "192.168.1.1"]

    if any(k in host for k in known_hosts):
        reachable = True

    rows = []
    sent = count
    received = 0

    for i in range(1, count + 1):

        # packet loss simulation
        loss_chance = random.random()

        if not reachable or loss_chance > 0.85:
            rows.append([
                i,
                f"Request timeout from {host}",
                "-",
                "-"
            ])
        else:
            ms = simulate_ping(host)
            ttl = random.choice([64, 128, 255])
            received += 1

            rows.append([
                i,
                f"Reply from {host}",
                f"{ms} ms",
                ttl
            ])

        time.sleep(0.05)  # small delay (UI realism)

    loss = round(((sent - received) / sent) * 100, 2)

    return {
        "success": True,
        "columns": TOOL_CONFIG["result_columns"],
        "rows": rows,
        "summary": {
            "host": host,
            "sent": sent,
            "received": received,
            "loss_percent": loss,
            "status": "REACHABLE" if received > 0 else "UNREACHABLE"
        }
    }