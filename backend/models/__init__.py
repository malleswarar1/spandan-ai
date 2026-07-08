"""SPANDAN AI — SQLAlchemy Models"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(100))
    email        = Column(String(200), unique=True, index=True)
    phone        = Column(String(20))
    hashed_pw    = Column(String(200))
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

class IdentityProfile(Base):
    __tablename__ = "identity_profiles"
    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, index=True)
    name          = Column(String(100))
    age           = Column(Integer)
    gender        = Column(String(20))
    education     = Column(String(50))
    occupation    = Column(String(100))
    pincode       = Column(String(10))
    state         = Column(String(50))
    district      = Column(String(100))
    languages     = Column(String(200))
    skills        = Column(Text)
    capital       = Column(Float)
    is_woman      = Column(Boolean, default=False)
    caste_category= Column(String(20))
    has_space     = Column(Boolean, default=False)
    risk_appetite = Column(String(20))
    opportunity_score = Column(Float, default=0.0)
    created_at    = Column(DateTime, default=datetime.utcnow)

class SavedOpportunity(Base):
    __tablename__ = "saved_opportunities"
    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, index=True)
    pincode       = Column(String(10))
    city          = Column(String(100))
    business_type = Column(String(100))
    match_score   = Column(Float)
    monthly_revenue = Column(Float)
    capital_needed  = Column(Float)
    result_json   = Column(Text)
    created_at    = Column(DateTime, default=datetime.utcnow)

class SpaceDesign(Base):
    __tablename__ = "space_designs"
    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, index=True)
    business_type = Column(String(100))
    total_area    = Column(Float)
    width_ft      = Column(Float)
    depth_ft      = Column(Float)
    budget        = Column(Float)
    design_json   = Column(Text)
    efficiency_score = Column(Float)
    created_at    = Column(DateTime, default=datetime.utcnow)
