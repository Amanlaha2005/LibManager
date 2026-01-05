# 📚 Library Management System (Django)

A role-based **Library Management System** built using **Python Django** with separate authentication for Students and Administrators. This project follows proper Django structure and GitHub version control practices.

---

## 📌 Project Overview

This project helps manage library users by providing:
- Separate login and registration for students and administrators
- Secure authentication
- Clean and responsive UI
- Scalable structure for future features

It is suitable for **college projects, internships, and job interviews**.

---

## 🚀 Features

### 👨‍🎓 Student Module
- Student Registration
- Student Login
- Profile image upload
- Secure authentication

### 🛠 Administrator Module
- Admin Registration
- Admin Login
- Separate admin authentication
- Profile image support

---

## 🧰 Tech Stack

- **Backend:** Python, Django  
- **Frontend:** HTML, CSS  
- **Database:** SQLite  
- **Version Control:** Git  
- **Repository:** GitHub  

---

---

## ⚙️ How to Run the Project

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Amanlaha2005/LibManager.git
cd LibManager

python -m venv env
env\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py migrate
python manage.py runserver
http://127.0.0.1:8000/

