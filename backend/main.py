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
    description="""
## SPANDAN AI — India's Business Opportunity Intelligence Platform

**Features:**
- 📍 **Location Intelligence** — Scan any of 200+ India pin codes for business gaps
- 🧠 **Opportunity Matching** — Match person to best business by capital, skills, demographics
- 🏗️ **Autonomous Space Designer** — Generate floor plans, equipment layout, cost estimates
- 👤 **Identity Profiler** — Full opportunity profile, govt scheme eligibility, skill gaps
- 💰 **Funding Finder** — Match to 12+ government schemes with EMI calculator
- 🔐 **Auth** — JWT-based register/login for saving results
    """,
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    contact={"name": "SPANDAN AI", "email": "hello@spandan.ai"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)

@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(round(time.time() - start, 4))
    response.headers["X-Powered-By"] = "SPANDAN AI v2"
    return response

from api.routes import opportunity, health, location, matching, funding, auth
from api.routes import space, identity

app.include_router(health.router,      prefix="/health",          tags=["Health"])
app.include_router(auth.router,        prefix="/api/auth",        tags=["Auth"])
app.include_router(location.router,    prefix="/api/location",    tags=["Location Intelligence"])
app.include_router(opportunity.router, prefix="/api/opportunity", tags=["Opportunity Scan"])
app.include_router(matching.router,    prefix="/api/match",       tags=["Business Matching"])
app.include_router(funding.router,     prefix="/api/funding",     tags=["Funding Schemes"])
app.include_router(space.router,       prefix="/api/space",       tags=["Space Designer"])
app.include_router(identity.router,    prefix="/api/identity",    tags=["Identity Profiler"])

@app.get("/")
async def root():
    return {
        "name": "SPANDAN AI",
        "sanskrit": "स्पन्दन",
        "tagline": "India's Pulse — Every Indian. Every Opportunity.",
        "version": "2.0.0",
        "docs": "/api/docs",
        "modules": {
            "location":    "/api/location",
            "opportunity": "/api/opportunity",
            "matching":    "/api/match",
            "funding":     "/api/funding",
            "space":       "/api/space",
            "identity":    "/api/identity",
            "auth":        "/api/auth",
        }
    }

@app.on_event("startup")
async def startup_event():
    logger.info("SPANDAN AI v2.0 starting up — India's Pulse Platform")
    try:
        from database import init_db
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"DB init skipped: {e}")
