from scapy.all import ARP, Ether, srp

TOOL_CONFIG = {
    "name": "Active IP Finder",
    "slug": "activeips",
    "description": "Find active devices in a network.",
    "icon": "bi-hdd-network",
    "button_text": "Find Devices",
    "fields": [
        {
            "name": "network_range",
            "label": "Network Range",
            "type": "text",
            "placeholder": "192.168.1.0/24",
            "required": True
        }
    ],
    "result_columns": ["IP Address", "MAC Address"]
}


def run(data):

    network_range = data.get("network_range", "").strip()

    if not network_range:
        return {
            "success": False,
            "error": "Network range is required"
        }

    try:

        arp_request = ARP(pdst=network_range)

        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

        packet = broadcast / arp_request

        answered = srp(packet, timeout=2, verbose=0)[0]

        rows = []

        for received in answered:

            rows.append([
                received[1].psrc,
                received[1].hwsrc
            ])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"Found {len(rows)} active devices"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }