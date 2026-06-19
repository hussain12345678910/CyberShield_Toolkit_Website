from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'main/index.html')


@login_required
def home_view(request):
    return render(request, 'main/home.html')


@login_required
def dashboard_view(request):
    return render(request, 'main/dashboard.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'main/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')   # 👈 change here

    return render(request, 'main/register.html')


def logout_view(request):
    logout(request)
    return redirect('index')


COMMON_TOOLS = [
    {'title': 'DNS Lookup Tool', 'desc': 'Fetch domain DNS records and IP mapping.', 'url': '/zunairatools/?tool=dns'},
    {'title': 'WHOIS Lookup', 'desc': 'Get domain registration details.', 'url': '/zunairatools/?tool=wis'},
    {'title': 'URL Safety Checker', 'desc': 'Check if URL is safe or malicious.', 'url': '/zunairatools/?tool=url'},
    {'title': 'System Info Tool', 'desc': 'View system hardware & OS info.', 'url': '/zunairatools/?tool=sysinfo'},
]
COMMON_TOOLS1 = [
    {
        'title': 'Caesar Cipher',
        'desc': 'Encrypt/Decrypt text',
        'url': '/ahsantools/?tool=caesar'
    },
    {
        'title': 'Make Hash',
        'desc': 'Generate MD5/SHA256',
        'url': '/ahsantools/?tool=hash'
    },
    {
        'title': 'Check Password',
        'desc': 'Validate password',
        'url': '/ahsantools/?tool=strength'
    },
    {
        'title': 'Random Password',
        'desc': 'Generate strong password',
        'url': '/ahsantools/?tool=password'
    }
]

COMMON_TOOLS3 = [
    {
        'title': 'Active IP Finder',
        'desc': 'Find active devices in network',
        'url': '/hussaintools/?tool=ip_finder'
    },
    {
        'title': 'Ping Tester',
        'desc': 'Check whether a host is reachable',
        'url': '/hussaintools/?tool=ping'
    },
    {
        'title': 'Port Scanner',
        'desc': 'Scan common ports',
        'url': '/hussaintools/?tool=portscan'
    },
    {
        'title': 'Packet Sniffer',
        'desc': 'Capture packets',
        'url': '/hussaintools/?tool=sniffer'
    }
]

COMMON_TOOLS4 = [
    {
        'title': 'File Integrity',
        'desc': 'Verify file changes using cryptographic hashing.',
        'url': '/unaizatools/?tool=fi'
    },
    {
        'title': 'Log Analyzer',
        'desc': 'Detect failed logins, errors and suspicious IP activity.',
        'url': '/unaizatools/?tool=log'
    },
    {
        'title': 'Duplicate File ',
        'desc': 'Find and analyze duplicate files using SHA256 hashing.',
        'url': '/unaizatools/?tool=dup'
    },
    {
        'title': 'File Meta',
        'desc': 'View file details like size, type, and timestamps.',
        'url': '/unaizatools/?tool=meta'
    }
]


@login_required
def zp_view(request):
    profile = {
        'initial': 'Z', 'name': 'Zunaira Arshad',
        'role': 'Project Lead / System Architect',
        'desc': 'Django frontend, UI design, dashboard system, tool integration, testing & full system audit.',
        'tools': COMMON_TOOLS,
    }
    return render(request, 'main/zp.html', {'profile': profile})


@login_required
def up_view(request):
    profile = {
        'initial': 'U', 'name': 'Unaiza Rehman',
        'role': 'File Security Developer',
        'desc': 'File integrity checker, log analyzer, duplicate file detection & metadata tools.',
        'tools': COMMON_TOOLS4,
    }
    return render(request, 'main/up.html', {'profile': profile})


@login_required
def ap_view(request):
    profile = {
        'initial': 'A', 'name': 'Ahsan',
        'role': 'Encryption Specialist',
        'desc': 'Encryption tools (Caesar, Hash), password utilities & cryptography modules.',
        'tools': COMMON_TOOLS1,
    }
    return render(request, 'main/ap.html', {'profile': profile})


@login_required
def hp_view(request):
    profile = {
        'initial': 'H', 'name': 'Hussain',
        'role': 'Backend Developer / API Engineer',
        'desc': 'API-based architecture, tool execution system, network tools development & backend endpoints.',
        'tools': COMMON_TOOLS3,
    }
    return render(request, 'main/hp.html', {'profile': profile})


@login_required
def zunaira_tools_view(request):
    return render(request, 'main/zunairatools.html')

@login_required
def unaiza_tools_view(request):
    return render(request, 'main/unaizatools.html')

@login_required
def ahsan_tools_view(request):
    return render(request, 'main/ahsantools.html')

@login_required
def hussain_tools_view(request):
    return render(request, 'main/hussaintools.html')


# def ahsantools(request):
#     tool = request.GET.get('tool')

#     if tool == 'cc':
#         return render(request, 'main/ahsan/cc.html')
#     elif tool == 'hg':
#         return render(request, 'main/ahsan/hg.html')
#     elif tool == 'pc':
#         return render(request, 'main/ahsan/pc.html')
#     elif tool == 'rp':
#         return render(request, 'main/ahsan/rp.html')

#     return render(request, 'main/ahsantools.html')

# def hussaintools(request):
#     tool = request.GET.get('tool')

#     if tool == 'activeips':
#         return render(request, 'main/hussain/ip-find.html')

#     elif tool == 'ping':
#         return render(request, 'main/hussain/ping.html')

#     elif tool == 'portscan':
#         return render(request, 'main/hussain/port-s.html')

#     elif tool == 'sniffer':
#         return render(request, 'main/hussain/psni.html')

#     return render(request, 'main/hussaintools.html')