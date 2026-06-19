import platform
import socket
import psutil

TOOL_CONFIG = {
    "name": "System Info",
    "slug": "sysinfo",
    "description": "Display detailed system, CPU, RAM, and network information of the host machine.",
    "icon": "bi-cpu",
    "button_text": "Get System Info",
    "fields": [],
    "result_columns": ["Property", "Value"]
}


def run(data):
    try:
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            ip = "N/A"

        mem = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)

        rows = [
            ["OS", platform.system()],
            ["Node Name", platform.node()],
            ["OS Release", platform.release()],
            ["OS Version", platform.version()[:60] + "..."],
            ["Machine", platform.machine()],
            ["Processor", platform.processor()[:60] + "..." if len(platform.processor()) > 60 else platform.processor()],
            ["CPU Cores", str(psutil.cpu_count(logical=True))],
            ["CPU Usage", f"{cpu_percent}%"],
            ["Total RAM", f"{round(mem.total / (1024**3), 2)} GB"],
            ["Used RAM", f"{round(mem.used / (1024**3), 2)} GB"],
            ["RAM Usage", f"{mem.percent}%"],
            ["Hostname", hostname],
            ["Local IP", ip],
        ]

        return {
            "success": True,
            "columns": TOOL_CONFIG["result_columns"],
            "rows": rows,
            "summary": f"System info collected from {hostname}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
