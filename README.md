# A4: Auth Login & Protect

## Overview

This project is a REST API built with **FastAPI** and **Supabase Authentication**. It provides user signup and login functionality, protected routes using Bearer access tokens, and token verification through Supabase.

## Technologies Used

* Python
* FastAPI
* Supabase Auth
* Uvicorn
* Python-dotenv
* HTTP Bearer Authentication

## Features

* User signup with email and password
* User login and access token generation
* Public information endpoint
* Protected profile endpoint
* Protected dashboard endpoint
* Access token verification using Supabase
* Logout endpoint
* Swagger UI documentation with Bearer authentication

## API Endpoints

| Method | Endpoint               | Description                               |
| ------ | ---------------------- | ----------------------------------------- |
| POST   | `/auth/signup`         | Register a new user                       |
| POST   | `/auth/login`          | Log in and receive an access token        |
| POST   | `/auth/logout`         | Log out through the API                   |
| GET    | `/public/info`         | Access public information                 |
| GET    | `/protected/profile`   | Retrieve the authenticated user's profile |
| GET    | `/protected/dashboard` | Access the protected dashboard            |

## Requirements

* Python 3.10 or later
* A Supabase project
* pip

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR-GITHUB-REPOSITORY-URL
cd flyrank-task-api-a4-auth
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install fastapi uvicorn python-dotenv supabase gotrue
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add your Supabase project credentials:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
```

Replace the placeholder values with your actual Supabase credentials. Never commit your `.env` file or expose your secret keys.

### 5. Run the application

```bash
uvicorn main:app --reload --port 8000
```

## API Documentation

Once the application is running, open:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication

1. Register a user using `POST /auth/signup`.
2. Log in using `POST /auth/login`.
3. Copy the returned access token.
4. Click **Authorize** in Swagger UI and enter the access token.
5. Use the token to access protected endpoints.

Protected routes require a valid access token. Missing, invalid, or expired tokens return an authentication error.

## Security Notes

* Environment variables are stored in `.env`.
* The `.env` file must not be committed to version control.
* Protected routes verify access tokens using Supabase Auth.

## Author

Judea Ann C. Tablate
