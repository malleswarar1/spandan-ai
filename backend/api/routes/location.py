"""SPANDAN AI — Location Intelligence Routes (v3 — 423+ pincodes)"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
router = APIRouter()

from ai_engine.data.india_pincodes import (
    PINCODE_DB, get as _get, suggest as _suggest,
    get_cities_by_state, TOTAL_PINCODES, ALL_STATES, search_by_city,
)

class LocationSearchRequest(BaseModel):
    pincode: str
    radius_km: Optional[float] = 5.0
    include_demographics: bool = True
    include_competitors: bool = True
    include_heatmap: bool = False

NEARBY_ZONES = {
    "metro":  ["Shopping malls within 5 km","Public transport hub","IT parks nearby","Dense residential blocks","Mixed commercial zone"],
    "tier1":  ["Busy market street","Residential colony","Auto/bus stand nearby","Local market cluster","Educational institutions"],
    "tier2":  ["Main market road","Town centre area","Government office zone","Bus depot nearby","Mixed residential-commercial"],
    "tier3":  ["Weekly haat market","District road junction","Mandal headquarters","Government hospital area","Agri-market outskirts"],
}

def _build_response(pincode: str, data: dict, profile, gaps) -> dict:
    tier = data.get("tier", "tier2")
    return {
        "pincode": pincode,
        "city": data["city"],
        "district": data.get("district", ""),
        "state": data["state"],
        "lat": data.get("lat", profile.lat),
        "lng": data.get("lng", profile.lng),
        "population": data.get("population", profile.population),
        "avg_income": data.get("avg_income", profile.avg_income),
        "income_tier": profile.income_tier,
        "city_tier": tier,
        "age_dominant": data.get("age_dominant", "working"),
        "literacy_rate": data.get("literacy_rate", 0.80),
        "commercial_density": data.get("commercial_density", 0.60),
        "opportunity_score": profile.opportunity_score,
        "nearby_zones": NEARBY_ZONES.get(tier, NEARBY_ZONES["tier2"]),
        "top_gaps": [
            {"type": g.business_type, "urgency": g.urgency,
             "monthly_revenue": g.estimated_monthly_revenue, "capital": g.min_capital_needed}
            for g in gaps[:8]
        ],
        "known": pincode in PINCODE_DB,
    }

@router.get("/pincode/{pincode}")
async def get_pincode_details(pincode: str):
    data = _get(pincode)
    if not data:
        data = {
            "city": f"Area-{pincode}", "district": "Unknown", "state": "India",
            "lat": 20.5937, "lng": 78.9629,
            "population": 50000, "avg_income": 500000,
            "age_dominant": "working", "tier": "tier2",
            "literacy_rate": 0.77, "commercial_density": 0.55,
        }
    from ai_engine.location.scanner import LocationScanner
    scanner = LocationScanner()
    profile = await scanner.scan_pincode(pincode)
    gaps = scanner.identify_gaps(profile)
    return _build_response(pincode, data, profile, gaps)

@router.post("/search")
async def search_location(req: LocationSearchRequest):
    return await get_pincode_details(req.pincode)

@router.get("/cities")
async def get_cities():
    cities_by_state = get_cities_by_state()
    # Also include tier distribution
    tier_counts: dict[str, int] = {}
    for entry in PINCODE_DB.values():
        tier_counts[entry["tier"]] = tier_counts.get(entry["tier"], 0) + 1
    return {
        "states": {
            state: [
                {"pincode": pin, "city": d["city"], "district": d.get("district",""),
                 "tier": d.get("tier","tier2"), "income": d["avg_income"],
                 "population": d["population"]}
                for pin, d in PINCODE_DB.items() if d["state"] == state
            ]
            for state in ALL_STATES
        },
        "all_states": ALL_STATES,
        "total_pincodes": TOTAL_PINCODES,
        "tier_distribution": tier_counts,
    }

@router.get("/states")
async def get_states():
    return {"states": ALL_STATES, "total": len(ALL_STATES)}

@router.get("/state/{state_name}")
async def get_by_state(state_name: str):
    matches = [
        {"pincode": pin, **d}
        for pin, d in PINCODE_DB.items()
        if d["state"].lower() == state_name.lower()
    ]
    if not matches:
        raise HTTPException(404, f"State '{state_name}' not found")
    return {"state": state_name, "pincodes": matches, "count": len(matches)}

@router.get("/heatmap")
async def opportunity_heatmap(limit: int = 50):
    profiles = []
    for pin, d in PINCODE_DB.items():
        pop_score = min(40, (d["population"] / 150000) * 40)
        inc_score = min(40, (d["avg_income"] / 2000000) * 40)
        den_score = min(20, d.get("commercial_density", 0.6) * 20)
        score = round(pop_score + inc_score + den_score, 1)
        profiles.append({
            "pincode": pin, "city": d["city"], "state": d["state"],
            "district": d.get("district", ""),
            "lat": d["lat"], "lng": d["lng"],
            "opportunity_score": score,
            "population": d["population"],
            "avg_income": d["avg_income"],
            "tier": d.get("tier", "tier2"),
        })
    profiles.sort(key=lambda x: -x["opportunity_score"])
    return {"heatmap": profiles[:limit], "total": len(profiles)}

@router.get("/suggest/{query}")
async def suggest_locations(query: str):
    results = _suggest(query, limit=10)
    return {
        "suggestions": [
            {"pincode": r["pincode"], "city": r["city"],
             "district": r.get("district", ""), "state": r["state"],
             "tier": r.get("tier", "tier2")}
            for r in results
        ]
    }

@router.get("/search-city")
async def search_by_city_name(q: str, limit: int = 10):
    results = search_by_city(q, limit)
    return {"results": results, "count": len(results)}

@router.get("/stats")
async def get_stats():
    tier_dist: dict[str, int] = {}
    income_sum = 0
    for d in PINCODE_DB.values():
        t = d.get("tier", "tier2")
        tier_dist[t] = tier_dist.get(t, 0) + 1
        income_sum += d["avg_income"]
    avg_income = round(income_sum / TOTAL_PINCODES) if TOTAL_PINCODES else 0
    return {
        "total_pincodes": TOTAL_PINCODES,
        "total_states": len(ALL_STATES),
        "tier_distribution": tier_dist,
        "average_income": avg_income,
        "states_covered": ALL_STATES,
    }
