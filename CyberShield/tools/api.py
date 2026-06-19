import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import dns_tool, wis_tool, url_tool, sysinfo_tool
# from tools.services.cc import caesar
# from tools.services.hg import make_hash
# from tools.services.pc import check_password
# from tools.services.rp import random_password


# from tools.services.ping_test import run as ping_test
# from tools.services.port_scanner import run as port_scanner
# from tools.services.packet_sniffer import run as packet_sniffer
# from tools.services.active_ip_finder import run as active_ip_finder
from .services import file_integrity, log_analyzer, duplicate_file_finder, file_metadata
from .services import caeser_cipher, hash_generator, Password_Strength_Checker,Random_Password_Generator
from .services import ip_finder, port_scanner,packet_sniffer,ping_tester

TOOL_MAP = {
    'dns': dns_tool,
    'wis': wis_tool,
    'url': url_tool,
    'sysinfo': sysinfo_tool,

    #   # 🔥 Ahsan tools
    # "cc": caesar,
    # "hg": make_hash,
    # "pc": check_password,
    # "rp": random_password,

       # 🔥 Ahsan tools
   "caesar": caeser_cipher,
    "hash": hash_generator,
    "strength": Password_Strength_Checker,
    "random": Random_Password_Generator,

    # hussain tools
    "ip_finder":ip_finder,
    "sniffer":port_scanner,
    "portscan":packet_sniffer,
    "ping":ping_tester,


     # Hussain tools
    # "ping": ping_test,
    # "portscan": port_scanner,
    # "sniffer": packet_sniffer,
    # "activeips": active_ip_finder,

    # =========================
    # FILE SECURITY SUITE (UNAIZA)
    # =========================
   "fi": file_integrity,
    "log": log_analyzer,
    "dup": duplicate_file_finder,
    "meta": file_metadata
}


def tool_config(request, tool_name):
    tool = TOOL_MAP.get(tool_name)
    if not tool:
        return JsonResponse({'error': 'Tool not found'}, status=404)
    return JsonResponse(tool.TOOL_CONFIG)


@csrf_exempt
@require_http_methods(["POST"])
def tool_execute(request, tool_name):
    tool = TOOL_MAP.get(tool_name)
    if not tool:
        return JsonResponse({'error': 'Tool not found'}, status=404)
    try:
        data = json.loads(request.body)
    except Exception:
        data = {}
    result = tool.run(data)
    return JsonResponse(result)
