from scapy.all import IP, ICMP, sr1

TOOL_CONFIG = {
    "name": "Ping Tester",
    "slug": "ping",
    "description": "Check whether a target host is reachable.",
    "icon": "bi-broadcast",
    "button_text": "Run Ping",
    "fields": [
        {
            "name": "target_ip",
            "label": "Target IP",
            "type": "text",
            "placeholder": "192.168.1.1",
            "required": True
        }
    ],
    "result_columns": ["Target IP", "Status"]
}


def run(data):
    target_ip = data.get("target_ip", "").strip()

    if not target_ip:
        return {"success": False, "error": "Target IP is required"}

    try:
        packet = IP(dst=target_ip) / ICMP()
        reply = sr1(packet, timeout=2, verbose=0)

        status = "Reachable" if reply else "Not Reachable"

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": [[target_ip, status]],
            "summary": f"Ping test completed for {target_ip}"
        }

    except Exception as e:
        return {"success": False, "error": str(e)}