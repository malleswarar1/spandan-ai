"""SPANDAN AI — Auth Routes (JWT)"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = ""

class LoginRequest(BaseModel):
    email: str
    password: str

class ProfileUpdateRequest(BaseModel):
    name:           Optional[str] = None
    phone:          Optional[str] = None
    age:            Optional[int] = None
    pincode:        Optional[str] = None
    state:          Optional[str] = None
    education:      Optional[str] = None
    skills:         Optional[str] = None
    capital:        Optional[float] = None
    is_woman:       Optional[bool] = None
    caste_category: Optional[str] = None
    risk_appetite:  Optional[str] = None
    languages:      Optional[str] = None

# In-memory user store (production would use DB)
_USERS: dict = {}  # email -> user record
_PROFILES: dict = {}  # email -> profile data

def _get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    from services import decode_token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    email = payload.get("sub")
    if not email or email not in _USERS:
        raise HTTPException(status_code=401, detail="User not found")
    return _USERS[email]

@router.post("/register")
async def register(req: RegisterRequest):
    if req.email in _USERS:
        raise HTTPException(status_code=400, detail="Email already registered")
    from services import hash_password, create_token
    hashed = hash_password(req.password)
    user = {"id": len(_USERS) + 1, "name": req.name, "email": req.email, "phone": req.phone, "hashed_pw": hashed}
    _USERS[req.email] = user
    _PROFILES[req.email] = {"name": req.name, "email": req.email, "phone": req.phone}
    token = create_token({"sub": req.email, "name": req.name})
    return {"access_token": token, "token_type": "bearer", "user": {"name": req.name, "email": req.email}}

@router.post("/login")
async def login(req: LoginRequest):
    user = _USERS.get(req.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    from services import verify_password, create_token
    if not verify_password(req.password, user["hashed_pw"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": req.email, "name": user["name"]})
    return {"access_token": token, "token_type": "bearer", "user": {"name": user["name"], "email": req.email}}

@router.get("/me")
async def get_me(current_user: dict = Depends(_get_current_user)):
    email = current_user["email"]
    profile = _PROFILES.get(email, {})
    return {"user": current_user, "profile": profile}

@router.put("/profile")
async def update_profile(req: ProfileUpdateRequest, current_user: dict = Depends(_get_current_user)):
    email = current_user["email"]
    profile = _PROFILES.get(email, {})
    for field, value in req.dict(exclude_none=True).items():
        profile[field] = value
    _PROFILES[email] = profile
    return {"message": "Profile updated", "profile": profile}

@router.post("/guest")
async def guest_session():
    """Create a short-lived guest session token"""
    from services import create_token
    from datetime import timedelta
    token = create_token({"sub": "guest@spandan.ai", "name": "Guest", "role": "guest"}, timedelta(hours=2))
    return {"access_token": token, "token_type": "bearer", "user": {"name": "Guest", "email": "guest@spandan.ai"}}
