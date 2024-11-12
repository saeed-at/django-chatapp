# Secure Chat Application
<div align="center">
    <img src="./assets/header.png" alt="Chat Application Header" width="100%" />
</div>

A real-time chat application built with Django, featuring end-to-end encryption, WebSocket communication, and Google Authentication.

## ✨ Key Features
- 🔒 End-to-end message encryption
- 🚀 Real-time messaging via WebSockets
- 🔑 Google OAuth2 Authentication
- 🌓 Dark/Light theme support
- 📱 Responsive design (Tailwind CSS)
- 🔍 Chatroom search functionality
- 🌐 RTL/LTR text direction auto-detection


## 🖼️ Preview

<details>
<summary><strong>View Screenshots</strong></summary>

### Welcome Page
New users are greeted with this page until authentication:
<div align="center">
    <img src="./assets/welcome.png" alt="Welcome Page" width="800px" />
</div>

### Chat Rooms Overview
Browse and join available chat rooms:
<div align="center">
    <img src="./assets/chatrooms.png" alt="Chat Rooms" width="800px" />
</div>

### Active Chat Interface
Real-time messaging with participant list:
<div align="center">
    <img src="./assets/chatpage.png" alt="Active Chat" width="800px" />
</div>

### Search Functionality
Find specific chat rooms instantly:
<div align="center">
    <img src="./assets/search-result.png" alt="Search Results" width="800px" />
</div>

### Admin Dashboard
Manage users, rooms, and permissions:
<div align="center">
    <img src="./assets/admin.png" alt="Admin Dashboard" width="800px" />
</div>

</details>

## 🛠️ Tech Stack

- **Backend**: Django + Channels (WebSocket support)
- **Database**: SQLite3
- **Security**: 
  - django-allauth (Authentication)
  - cryptography (E2E encryption)
  - WebSocket security protocols
- **Frontend**: 
  - Tailwind CSS
  - JavaScript
  - Responsive Design

## 🚀 Quick Start


### Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/saeed-at/django-chatapp.git
cd django-chatapp
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv

# Activate virtual environment
# For Linux/macOS:
source venv/bin/activate
# For Windows:
venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
Create `mysite/mysite/local_settings.py`:
```python
# Security Configuration
SECRET_KEY = 'your-django-secret-key'  # Change this!
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Encryption Configuration
ENCRYPTION_KEY = b'your-32-byte-encryption-key='  # Generate a secure key
```

5. **Set Up Authentication**
- Create admin account:
```bash
python manage.py createsuperuser
```
- [Configure Google OAuth2](https://www.youtube.com/watch?v=yO6PP0vEOMc)
  - Obtain client ID and secret
  - Configure OAuth consent screen
  - Add authorized redirect URIs

6. **Initialize Database**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Launch Application**
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


<div align="center">
    Made with ❤️ by <a href=https://github.com/saeed-at>saeed-at</a>
</div>

