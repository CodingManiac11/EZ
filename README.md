# Secure File Sharing System

## Overview
A secure file-sharing REST API system with two user types: Ops User (uploads files) and Client User (downloads files via secure, encrypted URLs). Includes email verification, JWT authentication, and file type restrictions.

## Tech Stack
- FastAPI
- SQLAlchemy (SQLite by default)
- JWT Auth
- Fernet encryption for secure URLs
- Pytest for testing

## Features
- Ops User: Login, upload pptx/docx/xlsx files
- Client User: Signup (with encrypted URL), email verification, login, list files, download files (secure URL)
- Secure, time-limited download links
- Role-based access control

## Setup
```sh
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate
pip install -r requirements.txt
```

---

## 1. Initialize the Database (Create Tables)
**Where:** Terminal (in your project root directory)

1. Activate your virtual environment:
   - **Windows:**
     ```sh
     venv\Scripts\activate
     ```
   - **Unix/Mac:**
     ```sh
     source venv/bin/activate
     ```
2. Start a Python shell:
   ```sh
   python
   ```
3. Run the following commands in the Python shell:
   ```python
   from app.models import Base
   from app.database import engine
   Base.metadata.create_all(bind=engine)
   exit()
   ```
   This will create all necessary tables in your SQLite database (`app.db`).

---

## 2. Create an Ops User Manually
**Where:** Python shell (after activating your virtual environment)

1. Start a Python shell:
   ```sh
   python
   ```
2. Run the following commands to create an Ops user:
   ```python
   from app.models import User
   from app.database import SessionLocal
   from app.auth import get_password_hash

   db = SessionLocal()
   user = User(email="ops@example.com", hashed_password=get_password_hash("opspass123"), is_active=True, is_ops=True)
   db.add(user)
   db.commit()
   db.close()
   exit()
   ```
   - You can change the email and password as needed.
   - This user will be able to log in and upload files as an Ops user.

---

## 3. Run the Server
**Where:** Terminal (in your project root directory, after activating your virtual environment)

```sh
uvicorn app.main:app --reload
```
- The server will start at `http://127.0.0.1:8000/` by default.
- You can now access the API endpoints using Postman or your browser.

---

## 4. Import the Postman Collection and Test All Endpoints
**Where:** Postman application

1. Open Postman (download from [https://www.postman.com/downloads/](https://www.postman.com/downloads/) if you don't have it).
2. Click **Import** (top left), then select the `postman_collection.json` file from your project directory.
3. Set the `baseUrl` variable in Postman to `http://127.0.0.1:8000` (or your server's address).
4. Use the provided requests to:
   - Log in as Ops user and upload files
   - Sign up as a Client user, verify email, log in, list files, get download links, and download files
   - Use the `Authorization` header with the JWT token returned from login endpoints for protected routes

---

## 5. Run Tests
**Where:** Terminal (in your project root directory, after activating your virtual environment)

```sh
pytest
```
- This will run the automated test suite to verify all main flows.

---

## Deployment
- Dockerize the app for production
- Use Gunicorn/Uvicorn with NGINX
- Store secrets in environment variables
- Use managed DB and object storage for production

## Postman
A Postman collection is provided in `postman_collection.json`. 