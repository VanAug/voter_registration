# Voter Registration System – Digital Recruitment

A scalable, mobile‑first voter registration platform that allows users to register via **USSD**, **WhatsApp**, and a **website**. Built with Django (backend) and React (frontend).

---

## 🚀 Features

- **Multi‑channel registration** – USSD, WhatsApp, and web form.
- **Centralised PostgreSQL database** – stores all applicants.
- **Admin dashboard** – view, search, filter, export to CSV, delete records (login protected).
- **Public status check** – anyone can check their registration by ID.
- **Production ready** – CORS, token authentication, environment variables.

---

## 📦 Tech Stack

### Backend
- Django 6.0 + Django REST Framework
- PostgreSQL (production) / SQLite (local)
- Token authentication (DRF)
- Africa’s Talking USSD SDK
- Twilio WhatsApp API
- Gunicorn (production server)

### Frontend
- React 19 + Vite
- Axios
- React Router
- CSS (mobile‑first)

---

## 🛠️ Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/voter-registration.git
cd voter-registration


2. Backend setup
bash

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Create a .env file in the backend/ directory (next to manage.py):
text

SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/voter_db

If using PostgreSQL locally, create the database:
sql

CREATE DATABASE voter_db;

Run migrations:
bash

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

3. Frontend setup
bash

cd frontend
npm install
npm run dev

The frontend will run on http://localhost:5173 and proxy API requests to Django (http://localhost:8000).
🌐 Deployment
Backend (Render)

    Push code to GitHub.

    Create a new Web Service on Render.

    Connect your repo, set:

        Build Command: pip install -r requirements.txt

        Start Command: gunicorn backend.backend_settings.wsgi:application

    Add environment variables (see below).

    Click Deploy.

Frontend (Vercel)

    Push frontend code to GitHub.

    Import project to Vercel.

    Add environment variable:

        VITE_API_BASE_URL = your Render backend URL (e.g., https://your-app.onrender.com)

    Deploy.

🔐 Environment Variables
Backend (settings.py reads from environment)
Variable	Description	Example
SECRET_KEY	Django secret key	django-insecure-...
DEBUG	Set to False in production	False
DATABASE_URL	PostgreSQL connection string	postgresql://user:pass@host:5432/db
ALLOWED_HOSTS	Comma‑separated domains	.onrender.com,localhost
CORS_ALLOWED_ORIGINS	Frontend URLs	https://your-app.vercel.app
CSRF_TRUSTED_ORIGINS	Same as above	same
AFRICASTALKING_USERNAME	Africa’s Talking sandbox username	sandbox
AFRICASTALKING_API_KEY	Your API key	atsk_...
TWILIO_ACCOUNT_SID	Twilio SID	AC...
TWILIO_AUTH_TOKEN	Twilio auth token	...
TWILIO_WHATSAPP_NUMBER	Twilio WhatsApp sandbox number	whatsapp:+14155238886
Frontend (Vercel / local)
Variable	Description
VITE_API_BASE_URL	Backend URL (e.g., https://your-backend.onrender.com)


📡 API Endpoints
Method	Endpoint	Description	Auth
POST	/api/register/web/	Website registration	No
POST	/api/register/whatsapp/	WhatsApp registration (internal)	No
POST	/api/register/ussd/simulate/	USSD simulation	No
POST	/api/ussd/callback/	Africa’s Talking USSD webhook	No
POST	/api/whatsapp/webhook/	Twilio WhatsApp webhook	No
GET	/api/applicants/	List all applicants	Token
DELETE	/api/applicants/<id>/	Delete applicant	Token
GET	/api/check-status/<id_number>/	Public status check	No

Authentication: For protected endpoints, include Authorization: Token <your-token> header.
📱 USSD Integration (Africa’s Talking)

    Create a USSD channel in your Africa’s Talking dashboard.

    Set the Callback URL to https://your-backend.onrender.com/api/ussd/callback/.

    Users dial *384*12345# (your shortcode) to start the menu.

    Flow: Menu → Register → Name → ID → County → Voter choice → Save.

💬 WhatsApp Integration (Twilio)

    Activate WhatsApp sandbox in Twilio.

    Set the webhook URL to https://your-backend.onrender.com/api/whatsapp/webhook/ (method POST).

    Users send MENU to the sandbox number.

    Flow: Menu → Register → Name → ID → County → Voter choice → Save.

🧪 Testing
Manual API test (curl)
bash

curl -X POST http://localhost:8000/api/register/web/ \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User","phone_number":"0712345678","id_number":"12345678","county":"Nairobi","voter_status":true}'

Run tests (if written)
bash

python manage.py test registration

📂 Project Structure
text

voter-registration/
├── backend/                     # Django project root
│   ├── backend/                 # project settings
│   │   ├── settings.py
│   │   └── urls.py
│   ├── registration/            # main app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views/
│   │   │   ├── api_views.py
│   │   │   ├── ussd_views.py
│   │   │   ├── whatsapp_views.py
│   │   │   └── status_views.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/                    # React app
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   ├── api.js
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.js
└── README.md

🐛 Troubleshooting
500 / 502 errors on WhatsApp webhook

    Ensure CACHES uses LocMemCache (no database table needed).

    Check Render logs for exceptions.

“relation does not exist”

    Switch to LocMemCache – no createcachetable required.

CORS errors

    Verify CORS_ALLOWED_ORIGINS includes your frontend domain.

USSD session resets

    Use LocMemCache and ensure only one worker runs (free tier).

📄 License

MIT – free for educational and commercial use.
👨‍💻 Author

Built as a developer test task for a digital recruitment system.

For questions, open an issue on GitHub.
text


Let me know if you need adjustments (e.g., more details on USSD session handling or deployment troubleshooting).

