# CyberShield

CyberShield is a Django-based web app that bundles a set of small cybersecurity / sysadmin utilities (password tools, network tools, file tools, etc.) behind a login-protected dashboard. Each contributor has their own profile page and tool dashboard, and tools are exposed both as web pages and as a simple JSON API.

## Features

- User accounts: register, login, logout (Django auth)
- Landing page, home page, and a main dashboard
- Per-contributor profile pages (Zunaira, Unaiza, Ahsan, Hussain)
- Per-contributor tool dashboards, each linking to a set of tools, including:
  - Password strength checker / random password generator
  - Hash generator, Caesar cipher
  - DNS lookup tool, WHOIS tool, URL/IP tools
  - Port scanner, ping tester, packet sniffer
  - File integrity checker, file metadata viewer, duplicate file finder
  - System info tool, log analyzer
- A small internal API (`/api/tool-config/<tool>/` and `/api/tools/<tool>/`) so tools can be driven from the front end via JSON

## Tech Stack

- Python 3 + Django 4.2+
- SQLite (default database, file already included as `db.sqlite3`)
- Vanilla HTML/CSS/JS templates (no frontend framework)

## Project Structure

```
cybershield/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── config/          # Django project settings, URLs, WSGI
├── main/            # Auth, pages, profiles, tool dashboards
├── tools/           # Tool logic (tools/services/*.py) + API (api.py, views.py)
├── static/          # CSS, JS, images
└── templates/        # Base template
```

---

## Setup From Scratch

These steps assume you are starting with nothing installed except a computer. Follow them in order.

### 1. Install Python

You need Python 3.10+ (the project was built against 3.13).

- **Windows:** download from https://www.python.org/downloads/ and run the installer. Tick "Add Python to PATH" during install.
- **macOS:** `brew install python3` (requires Homebrew), or download from python.org.
- **Linux:** `sudo apt install python3 python3-venv python3-pip` (Debian/Ubuntu) or your distro's equivalent.

Verify it worked:
```bash
python3 --version
```

### 2. Get the project files

If you received this as a zip, extract it. If it's a git repo:
```bash
git clone <repo-url>
cd cybershield
```

### 3. Create a virtual environment

A virtual environment keeps this project's Python packages separate from the rest of your system.

```bash
python3 -m venv venv
```

Activate it:

- **Windows (cmd):** `venv\Scripts\activate.bat`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **macOS/Linux:** `source venv/bin/activate`

You'll know it worked because your terminal prompt will show `(venv)` at the start.

> Note: this project's zip already ships a `venv/` folder. It's safer to ignore that one and create your own fresh environment as shown above, since a venv built on someone else's machine often won't work correctly on yours.

### 4. Install dependencies

With the virtual environment active:

```bash
pip install -r requirements.txt
```

This installs Django, dnspython, python-whois, requests, and psutil.

### 5. Apply database migrations

Django needs to set up its internal tables (auth, sessions, etc.) in the database:

```bash
python manage.py migrate
```

### 6. Create an admin user (optional but recommended)

This lets you log into Django's admin panel at `/admin/`:

```bash
python manage.py createsuperuser
```
Follow the prompts (username, email, password).

### 7. Run the development server

```bash
python manage.py runserver
```

You should see output ending in something like:
```
Starting development server at http://127.0.0.1:8000/
```

### 8. Open it in your browser

Go to **http://127.0.0.1:8000/**

- If you're not logged in, you'll land on the index/landing page.
- Click **Register** to create an account, or **Login** if you already have one.
- After logging in you'll be redirected to `/home/`.

### 9. (Production only) Collect static files

Only needed when deploying for real users, not for local development:

```bash
python manage.py collectstatic
```

---

## URL Map

| URL | Purpose |
|---|---|
| `/` | Landing page (redirects to `/home/` if logged in) |
| `/home/` | Home page (login required) |
| `/dashboard/` | Main dashboard (login required) |
| `/login/` | Login |
| `/register/` | Register |
| `/logout/` | Logout |
| `/profile/zunaira/`, `/profile/unaiza/`, `/profile/ahsan/`, `/profile/hussain/` | Contributor profile pages |
| `/zunairatools/`, `/unaizatools/`, `/ahsantools/`, `/hussaintools/` | Contributor tool dashboards |
| `/api/tool-config/<tool_name>/` | GET — returns a tool's config as JSON |
| `/api/tools/<tool_name>/` | POST — runs a tool and returns its result as JSON |

## Adding a New Tool

1. Create `tools/services/mytool.py` exposing a `TOOL_CONFIG` dict and a `run(data)` function.
2. Import it in `tools/api.py` and register it in `TOOL_MAP`.
3. Add a card for it on the relevant dashboard template (e.g. `zunairatools.html`) and a sidebar nav link.

## Common Issues

- **`python manage.py` fails with "No module named django"** → your virtual environment isn't activated, or dependencies weren't installed. Redo steps 3–4.
- **Port already in use** → run `python manage.py runserver 8001` to use a different port.
- **Static files (CSS/JS) not loading** → make sure `DEBUG = True` in `config/settings.py` for local dev, and that you're running through `runserver`, not opening HTML files directly in the browser.
- **Database errors / missing tables** → run `python manage.py migrate` again.

## Security Notes (before deploying anywhere public)

The project ships with development defaults that are **not safe for production**:
- `SECRET_KEY` in `config/settings.py` is a placeholder — replace it.
- `DEBUG = True` — set to `False` in production.
- `ALLOWED_HOSTS = ['*']` — restrict to your actual domain.
- `CSRF_COOKIE_SECURE` / `SESSION_COOKIE_SECURE` are `False` — set to `True` once served over HTTPS.

Several tools here (port scanner, packet sniffer, ping tester) perform real network operations — only point them at hosts/networks you own or have permission to test.
