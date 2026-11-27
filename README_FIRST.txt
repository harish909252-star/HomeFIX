HOMEFIX COMPLETE DJANGO PROJECT
================================

This ZIP contains a complete project source layout assembled from the files
you uploaded: home.html, views.py, models.py, settings.py, urls.py, wsgi.py,
manage.py, and the supplied HomeFix admin/dashboard package.

IMPORTANT BEFORE USING
----------------------
1. Back up your current project folder and db.sqlite3 first.
2. Extract this ZIP to a NEW folder. Do not extract over your current project.
3. Copy your existing .venv folder only if you want to reuse it and its Python
   version is compatible. Otherwise create a fresh environment.
4. Copy your existing static/images assets into static/images. The page expects:
   - homefix-hero.jpeg
   - washing machine.jpeg
   - refrigerator(fridge).jpeg
   - ac.jpeg
5. This ZIP does not contain your existing database or .venv. Keep your current
   db.sqlite3 safe. If you already have bookings, do not replace your database.
6. The project uses the `homefix` settings package and `services` Django app.

RUN ON WINDOWS POWERSHELL
-------------------------
Open PowerShell in the extracted folder (the folder containing manage.py):

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python manage.py check
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

If PowerShell blocks activation, you can avoid activation and run:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe manage.py check
    .\.venv\Scripts\python.exe manage.py migrate
    .\.venv\Scripts\python.exe manage.py runserver

OPEN IN CHROME
--------------
Home:       http://127.0.0.1:8000/
Admin:      http://127.0.0.1:8000/admin/
Dashboard:  http://127.0.0.1:8000/service/dashboard/

Dashboard requires a staff/superuser login.

BOOKING / CSRF
--------------
The home page form posts to the Django book_service URL and includes
{% csrf_token %}. Keep CsrfViewMiddleware enabled. Do not disable CSRF.

WHATSAPP
--------
The admin package has optional Twilio WhatsApp notifications. Status updates
are saved even if WhatsApp is not configured; a warning is shown. To enable
WhatsApp, install `twilio` and configure TWILIO_ACCOUNT_SID,
TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_FROM as environment variables/settings.

DATABASE CAUTION
----------------
The ZIP does not include a database. `migrate` creates a new database if one
does not exist. To retain old bookings, copy your existing db.sqlite3 into
the project root only after confirming it belongs to this same project/model.
