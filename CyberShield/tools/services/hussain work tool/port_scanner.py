from scapy.all import IP, TCP, sr1, send

TOOL_CONFIG = {
    "name": "Port Scanner",
    "slug": "portscan",
    "description": "Scan common ports of a target machine.",
    "icon": "bi-diagram-3",
    "button_text": "Scan Ports",
    "fields": [
        {
            "name": "target_ip",
            "label": "Target IP",
            "type": "text",
            "placeholder": "192.168.1.1",
            "required": True
        }
    ],
    "result_columns": ["Port", "Status"]
}


def run(data):

    target_ip = data.get("target_ip", "").strip()

    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445]

    rows = []

    try:

        for port in ports:

            packet = IP(dst=target_ip) / TCP(dport=port, flags="S")

            response = sr1(packet, timeout=1, verbose=0)

            if response:

                if response.haslayer(TCP):

                    if response[TCP].flags == 0x12:

                        rows.append([port, "OPEN"])

                        send(
                            IP(dst=target_ip) /
                            TCP(dport=port, flags="R"),
                            verbose=0
                        )

                    elif response[TCP].flags == 0x14:

                        rows.append([port, "CLOSED"])

            else:

                rows.append([port, "FILTERED"])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"Scanned {len(ports)} ports"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }