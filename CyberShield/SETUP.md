# CyberShield Django Setup Instructions

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Apply Migrations
```bash
python manage.py migrate
```

## 3. Create Superuser (optional)
```bash
python manage.py createsuperuser
```

## 4. Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## 5. Run Development Server
```bash
python manage.py runserver
```

## URL Routes
| URL | View |
|-----|------|
| / | Landing page (redirects to /home if logged in) |
| /home/ | Home page (login required) |
| /dashboard/ | Dashboard (login required) |
| /login/ | Login |
| /register/ | Register |
| /logout/ | Logout |
| /profile/zunaira/ | Zunaira's profile |
| /profile/unaiza/ | Unaiza's profile |
| /profile/ahsan/ | Ahsan's profile |
| /profile/hussain/ | Hussain's profile |
| /zunairatools/ | ZunairaTools dashboard |
| /api/tool-config/<tool>/ | GET tool config JSON |
| /api/tools/<tool>/ | POST execute tool |

## Adding a New Tool
1. Create `tools/services/mytool.py` with `TOOL_CONFIG` dict and `run(data)` function
2. Import it in `tools/api.py` and add to `TOOL_MAP`
3. Add a card in `zunairatools.html` and a nav link in the sidebar
