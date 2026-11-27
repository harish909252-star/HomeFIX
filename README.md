# 🏠 HomeFIX – Home Appliance Service Website

A Django-based Home Appliance Service Booking Website developed using Python, Django, HTML, CSS, JavaScript, and SQLite.

## 📌 About the Project

HomeFIX is a web-based platform that allows customers to book home appliance repair and maintenance services easily.

Customers can submit service requests, provide their address, select appliances, and choose their preferred booking date and time.

## ✨ Features

- Online Service Booking
- Washing Machine Repair
- Refrigerator Repair
- Air Conditioner (AC) Service
- Customer Details Management
- Booking Date and Time Selection
- Booking Status Management
- Admin Dashboard
- Service Area Information
- Responsive Website Design

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Django | Web Framework |
| HTML5 | Website Structure |
| CSS3 | Website Styling |
| JavaScript | Interactive Elements |
| SQLite | Database |
| Git & GitHub | Version Control |

## 📂 Project Structure

```text
HomeFIX/
│
├── homefix/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── services/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── static/
│   └── images/
│
├── templates/
│   └── home.html
│
├── manage.py
├── requirements.txt
├── RUN_HOMEFIX.bat
└── .gitignore
```

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/harish909252-star/HomeFIX.git
```

### 2. Open Project Folder

```bash
cd HomeFIX
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Requirements

```bash
pip install -r requirements.txt
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Start Development Server

```bash
python manage.py runserver
```

Open your browser:

http://127.0.0.1:8000/

## 👨‍💻 Developer

**Harish Kumar**

Python Full Stack Developer | Fresher

📍 Madurai, Tamil Nadu, India

GitHub: https://github.com/harish909252-star

## 📄 License

This project is developed for learning and educational purposes.
