from fastapi import APIRouter
from datetime import datetime
import sys, os

router = APIRouter()

@router.get("/")
async def health():
    try:
        from ai_engine.data.india_pincodes import TOTAL_PINCODES, ALL_STATES
        db_info = {"total_pincodes": TOTAL_PINCODES, "states_covered": len(ALL_STATES)}
    except Exception:
        db_info = {"total_pincodes": 0, "states_covered": 0}
    return {
        "status": "healthy",
        "service": "SPANDAN AI",
        "version": "3.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "modules": ["location", "opportunity", "matching", "funding", "space", "identity", "auth"],
        "database": db_info,
    }

@router.get("/ready")
async def readiness():
    checks = {}
    try:
        from ai_engine.location.scanner import LocationScanner
        LocationScanner()
        checks["location_scanner"] = "ok"
    except Exception as e:
        checks["location_scanner"] = str(e)
    try:
        from ai_engine.matching.matcher import PersonBusinessMatcher
        PersonBusinessMatcher()
        checks["matcher"] = "ok"
    except Exception as e:
        checks["matcher"] = str(e)
    try:
        from ai_engine.space.designer import SpaceDesigner
        SpaceDesigner()
        checks["space_designer"] = "ok"
    except Exception as e:
        checks["space_designer"] = str(e)
    try:
        from ai_engine.identity.profiler import IdentityProfiler
        IdentityProfiler()
        checks["identity_profiler"] = "ok"
    except Exception as e:
        checks["identity_profiler"] = str(e)
    all_ok = all(v == "ok" for v in checks.values())
    return {"ready": all_ok, "checks": checks, "timestamp": datetime.utcnow().isoformat()}
