import random
from datetime import datetime

TOOL_CONFIG = {
    "name": "Packet Sniffer",
    "slug": "sniffer",
    "description": "Simulated network packet capture tool",
    "icon": "bi-wifi",
    "button_text": "Start Capture",
    "fields": [
        {
            "name": "protocol",
            "label": "Protocol Filter",
            "type": "select",
            "options": ["ALL", "TCP", "UDP", "ICMP", "ARP", "DNS", "HTTP"]
        },
        {
            "name": "count",
            "label": "Packet Count",
            "type": "number",
            "placeholder": "e.g. 10",
            "required": True
        }
    ],
    "result_columns": ["#", "Time", "Protocol", "Source", "Destination", "Length", "Summary"]
}

PROTOCOLS = ["TCP", "UDP", "ICMP", "ARP", "DNS", "HTTP"]

IPS = [
    "192.168.1.1",
    "192.168.1.10",
    "10.0.0.5",
    "172.16.0.4",
    "8.8.8.8",
    "1.1.1.1",
    "185.60.216.53"
]


def rand_ip():
    return random.choice(IPS)


def rand_port():
    return random.choice([21, 22, 80, 443, 53, 8080, 3306, 110])


def rand_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def generate_summary(proto, src, dst, length):
    if proto in ["TCP", "HTTP"]:
        return f"{src}:{rand_port()} > {dst}:{rand_port()} [TCP Stream] Len={length}"

    elif proto in ["UDP", "DNS"]:
        return f"{src} > {dst} DNS Query Len={length}"

    elif proto == "ICMP":
        return f"{src} > {dst} ICMP Echo Request id={random.randint(1,999)}"

    elif proto == "ARP":
        return f"ARP Request: who-has {dst} tell {src}"

    else:
        return f"{proto} Packet {src} -> {dst} Len={length}"


def run(data):
    try:
        count = int(data.get("count", 10))
        protocol = data.get("protocol", "ALL").upper()

        rows = []

        for i in range(1, count + 1):

            proto = protocol if protocol != "ALL" else random.choice(PROTOCOLS)

            src = rand_ip()
            dst = rand_ip()

            while dst == src:
                dst = rand_ip()

            length = random.randint(40, 1500)
            time = rand_time()

            summary = generate_summary(proto, src, dst, length)

            rows.append([
                i,
                time,
                proto,
                src,
                dst,
                length,
                summary
            ])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"Captured {count} packets ({protocol})"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }