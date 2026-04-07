# Voter Registration System – Digital Recruitment

A scalable, mobile‑first voter registration platform that allows users to register via **USSD**, **WhatsApp**, and a **website**. Built with Django (backend) and React (frontend).

---

## Features

- **Multi‑channel registration** – USSD, WhatsApp, and web form.
- **Centralised PostgreSQL database** – stores all applicants.
- **Admin dashboard** – view, search, filter, export to CSV, delete records (login protected).
- **Public status check** – anyone can check their registration by ID.
- **Production ready** – CORS, token authentication, environment variables.

---

To access whatsapp bot:
 send join frighten-zebra to whatsapp number +1 415 523 8886
 send "menu" for options 

to register through ussd:
 dial *384*99767#

## Tech Stack

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

If using PostgreSQL locally, create the database:

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

Deployment
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


📂 Project Structure

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



