from scapy.all import sniff

TOOL_CONFIG = {
    "name": "Packet Sniffer",
    "slug": "sniffer",
    "description": "Capture network packets.",
    "icon": "bi-wifi",
    "button_text": "Start Capture",
    "fields": [],
    "result_columns": ["#", "Packet Summary"]
}


def run(data):

    packets = []

    def packet_callback(packet):
        packets.append(packet.summary())

    try:

        sniff(prn=packet_callback, count=10)

        rows = []

        for i, pkt in enumerate(packets, 1):
            rows.append([i, pkt])

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": "Captured 10 packets"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }