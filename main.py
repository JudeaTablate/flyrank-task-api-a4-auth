
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from gotrue.errors import AuthApiError


# ============================================================
# STAGE 0: SETUP AND SUPABASE CONNECTION
# ============================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PORT = int(os.getenv("PORT", "8000"))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in the .env file."
    )

# Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create FastAPI application
app = FastAPI(
    title="FlyRank Auth API",
    description="A secure authentication API using FastAPI and Supabase Auth.",
    version="1.0.0",
)

# Bearer authentication scheme for protected routes
security = HTTPBearer(auto_error=False)


# ============================================================
# REQUEST MODEL
# ============================================================

class AuthCredentials(BaseModel):
    email: str | None = None
    password: str | None = None


# ============================================================
# STAGE 0: BASIC ROUTES
# ============================================================

@app.get("/")
def root():
    return {
        "message": "FlyRank Auth API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "supabase_configured": True,
    }


# ============================================================
# STAGE 1: SIGN UP
# ============================================================

@app.post("/auth/signup", status_code=201)
def signup(body: AuthCredentials | None = None):

    if (
        body is None
        or not body.email
        or not body.email.strip()
        or not body.password
        or not body.password.strip()
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"},
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": body.email.strip(),
                "password": body.password,
            }
        )

        if response.user is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Signup failed"},
            )

        return JSONResponse(
            status_code=201,
            content=jsonable_encoder(response.user),
        )

    except AuthApiError:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Signup failed. Check the email and password."
            },
        )


# ============================================================
# STAGE 1: LOG IN
# ============================================================

@app.post("/auth/login")
def login(body: AuthCredentials | None = None):

    if (
        body is None
        or not body.email
        or not body.email.strip()
        or not body.password
        or not body.password.strip()
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"},
        )

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": body.email.strip(),
                "password": body.password,
            }
        )

        if response.session is None:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid login credentials"},
            )

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }

    except AuthApiError:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"},
        )


# ============================================================
# STAGE 2: PUBLIC ROUTE
# ============================================================

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


# ============================================================
# STAGE 3: VERIFIED PROTECTED PROFILE ROUTE
# ============================================================

@app.get("/protected/profile")
def protected_profile(
    credentials: HTTPAuthorizationCredentials | None = Depends(security)
):

    # Check whether a Bearer token was provided
    if credentials is None:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"},
        )

    # Extract the access token
    token = credentials.credentials

    if not token.strip():
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"},
        )

    try:
        # Ask Supabase to validate the JWT and retrieve the user
        response = supabase.auth.get_user(token)

        user = response.user

        if user is None:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid or expired token"},
            )

        # Return verified user information
        return {
            "id": str(user.id),
            "email": user.email,
            "created_at": user.created_at,
        }

    except AuthApiError:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or expired token"},
        )