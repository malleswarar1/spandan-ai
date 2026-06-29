from fastapi import APIRouter
from datetime import datetime
router = APIRouter()

@router.get("/")
async def health():
    return {
        "status": "healthy",
        "service": "SPANDAN AI",
        "timestamp": datetime.utcnow().isoformat()
    }
