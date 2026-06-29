"""SPANDAN AI — Opportunity API Route"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../'))

router = APIRouter()

class OpportunityRequest(BaseModel):
    pincode: str
    capital: float
    skills: list = ["any"]
    education: str = "10th"
    language: str = "Hindi"
    has_space: bool = False
    risk_appetite: str = "medium"
    is_woman: bool = False
    caste_category: str = "general"
    age: int = 30
    name: str = "User"

@router.post("/scan")
async def scan_opportunity(request: OpportunityRequest):
    try:
        from ai_engine.location.scanner import LocationScanner
        from ai_engine.matching.matcher import PersonBusinessMatcher, PersonProfile

        scanner = LocationScanner()
        matcher = PersonBusinessMatcher()
        profile = await scanner.scan_pincode(request.pincode)
        gaps    = scanner.identify_gaps(profile)
        person  = PersonProfile(
            name=request.name, pincode=request.pincode,
            capital=request.capital, skills=request.skills,
            education=request.education, language=request.language,
            has_space=request.has_space, risk_appetite=request.risk_appetite,
            is_woman=request.is_woman, caste_category=request.caste_category,
            age=request.age,
        )
        matches = matcher.match(person, gaps, top_n=5)
        return {
            "pincode": profile.pincode,
            "city": profile.city,
            "state": profile.state,
            "opportunity_score": profile.opportunity_score,
            "population": profile.population,
            "income_tier": profile.income_tier,
            "top_gaps": [{
                "business_type": g.business_type,
                "urgency": g.urgency,
                "monthly_revenue": g.estimated_monthly_revenue,
                "capital_needed": g.min_capital_needed,
                "competition": g.competition_level,
            } for g in gaps[:10]],
            "matched_businesses": [{
                "business_type": m.business_type,
                "match_score": m.match_score,
                "monthly_revenue": m.monthly_revenue_estimate,
                "capital_needed": m.capital_needed,
                "capital_gap": m.capital_gap,
                "funding_schemes": m.funding_schemes,
                "setup_steps": m.setup_steps,
                "location_advice": m.location_advice,
                "success_probability": m.success_probability,
            } for m in matches],
            "message": f"Found {len(gaps)} opportunities in {profile.city}",
            "message_hindi": f"{profile.city} mein {len(gaps)} vyapar ke avsar mile",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/city/{city_name}")
async def city_opportunities(city_name: str):
    cities = {
        "bangalore": ["560001","560037","560066","560100"],
        "mumbai":    ["400001"],
        "delhi":     ["110001"],
        "hyderabad": ["500001"],
        "chennai":   ["600001"],
    }
    pincodes = cities.get(city_name.lower())
    if not pincodes:
        raise HTTPException(status_code=404, detail=f"City {city_name} not found")
    from ai_engine.location.scanner import LocationScanner
    scanner = LocationScanner()
    results = await scanner.scan_city(pincodes)
    return {
        "city": city_name,
        "pincodes_scanned": len(pincodes),
        "results": {
            pin: {
                "opportunity_score": data["profile"].opportunity_score,
                "top_gaps": [{"type": g.business_type, "urgency": g.urgency, "revenue": g.estimated_monthly_revenue} for g in data["gaps"][:5]]
            }
            for pin, data in results.items()
        }
    }
