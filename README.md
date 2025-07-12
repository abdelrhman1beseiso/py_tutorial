# 🐍 Python Tutorial Platform

A web-based learning platform built with Django to help students learn Python through structured chapters and topics. The platform supports two user roles — **students** and **admins** — each with dedicated functionality.

---

## 👥 User Roles

### 👨‍🎓 Student (Custom User)
- **Sign Up / Log In / Password Reset** via the `account` templates.
- Access a clean learning dashboard.
- View available **chapters** and their **topics**.
- Track learning progress via the `progress.html` interface.

### 🛠️ Admin
- Manage educational content via the `admin` templates.
- Create, edit, and delete **chapters** and **topics**.
- Chapters can contain Markdown-formatted content (.md).
- Access to an **admin dashboard** for content and user control.

---

## 🗂️ Template Structure

### `templates/account/`
- Handles authentication: `login.html`, `signup.html`, and all password reset views.

### `templates/admin/`
- Admin control views: `chapter_form.html`, `topic_form.html`, `dashboard.html`, `delete.html`.

### `UserApp/templates/`
- Student-facing UI: `home.html`, `chapter_list.html`, `chapter_detail.html`, `topic_detail.html`, and `progress.html`.

---

## 💡 Features

- 🔐 Custom user authentication (students only).
- 🧠 Structured learning through chapters & topics.
- 📈 Trackable student progress.
- 📄 Markdown-based content formatting.
- ⚙️ Full CRUD operations for admin.
- 💼 Separate interfaces for students and admins.

---

## 🏁 Getting Started

### Requirements
- Python 3.8+
- Django 3.0+
- Markdown support (e.g. `markdown2`)

### Setup Instructions
```bash
git clone <your-repo-url>
cd python-tutorial-platform
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
