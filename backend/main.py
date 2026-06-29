"""SPANDAN AI — स्पन्दन — Main Application"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time, logging, sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spandan")

app = FastAPI(
    title="SPANDAN AI — स्पन्दन",
    description="India's Business Opportunity Intelligence Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(round(time.time() - start, 4))
    return response

from api.routes import opportunity, health, location, matching, funding, auth

app.include_router(health.router,      prefix="/health",          tags=["Health"])
app.include_router(auth.router,        prefix="/api/auth",        tags=["Auth"])
app.include_router(location.router,    prefix="/api/location",    tags=["Location"])
app.include_router(opportunity.router, prefix="/api/opportunity", tags=["Opportunity"])
app.include_router(matching.router,    prefix="/api/match",       tags=["Matching"])
app.include_router(funding.router,     prefix="/api/funding",     tags=["Funding"])

@app.get("/")
async def root():
    return {
        "name": "SPANDAN AI",
        "sanskrit": "स्पन्दन",
        "tagline": "India's Pulse — Every Indian. Every Opportunity.",
        "version": "1.0.0",
        "docs": "/api/docs"
    }
