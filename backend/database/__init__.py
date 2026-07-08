"""SPANDAN AI — Database Layer (SQLite with pincode seeding)"""
import os
import logging
import sys

log = logging.getLogger("spandan.db")

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./spandan.db")

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    if DB_URL.startswith("sqlite"):
        engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(DB_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    _SQLALCHEMY_OK = True
except ModuleNotFoundError:
    _SQLALCHEMY_OK = False
    engine = None
    SessionLocal = None
    Base = object

def get_db():
    if not _SQLALCHEMY_OK:
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    if not _SQLALCHEMY_OK:
        log.warning("DB init skipped: sqlalchemy not installed")
        return
    try:
        Base.metadata.create_all(bind=engine)
        _seed_pincodes()
        log.info("DB initialised successfully")
    except Exception as e:
        log.warning(f"DB init error (non-fatal): {e}")

def _seed_pincodes():
    """Seed pincode data into SQLite for fast SQL queries."""
    if not _SQLALCHEMY_OK:
        return
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
        from ai_engine.data.india_pincodes import PINCODE_DB

        with engine.connect() as conn:
            # Create pincodes table if not exists
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS pincodes (
                    pincode     TEXT PRIMARY KEY,
                    city        TEXT,
                    district    TEXT,
                    state       TEXT,
                    lat         REAL,
                    lng         REAL,
                    population  INTEGER,
                    avg_income  INTEGER,
                    age_dominant TEXT,
                    tier        TEXT,
                    literacy_rate REAL,
                    commercial_density REAL
                )
            """))

            # Create users, opportunities, designs tables
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT,
                    email       TEXT UNIQUE,
                    phone       TEXT,
                    hashed_pw   TEXT,
                    is_active   INTEGER DEFAULT 1,
                    created_at  TEXT DEFAULT (datetime('now'))
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS saved_opportunities (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id     INTEGER,
                    pincode     TEXT,
                    business_type TEXT,
                    match_score REAL,
                    result_json TEXT,
                    created_at  TEXT DEFAULT (datetime('now'))
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS space_designs (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id     INTEGER,
                    business_type TEXT,
                    area        REAL,
                    design_json TEXT,
                    created_at  TEXT DEFAULT (datetime('now'))
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS search_analytics (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    pincode     TEXT,
                    module      TEXT,
                    timestamp   TEXT DEFAULT (datetime('now'))
                )
            """))

            # Seed pincodes (upsert)
            existing = conn.execute(text("SELECT COUNT(*) FROM pincodes")).scalar()
            if existing < len(PINCODE_DB):
                for pin, entry in PINCODE_DB.items():
                    conn.execute(text("""
                        INSERT OR REPLACE INTO pincodes
                        (pincode,city,district,state,lat,lng,population,avg_income,age_dominant,tier,literacy_rate,commercial_density)
                        VALUES (:pin,:city,:dist,:state,:lat,:lng,:pop,:inc,:age,:tier,:lit,:den)
                    """), {
                        "pin": pin, "city": entry["city"], "dist": entry.get("district",""),
                        "state": entry["state"], "lat": entry["lat"], "lng": entry["lng"],
                        "pop": entry["population"], "inc": entry["avg_income"],
                        "age": entry["age_dominant"], "tier": entry["tier"],
                        "lit": entry.get("literacy_rate", 0.80), "den": entry.get("commercial_density", 0.60),
                    })
                conn.commit()
                log.info(f"Seeded {len(PINCODE_DB)} pincodes into SQLite")
            else:
                log.info(f"Pincodes already seeded ({existing} rows)")
    except Exception as e:
        log.warning(f"Pincode seeding skipped: {e}")
