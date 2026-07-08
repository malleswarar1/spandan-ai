"""SPANDAN AI — Matching Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
router = APIRouter()

class MatchRequest(BaseModel):
    pincode: str
    capital: float
    skills: List[str] = ["any"]
    education: str = "10th"
    language: str = "Hindi"
    has_space: bool = False
    risk_appetite: str = "medium"
    is_woman: bool = False
    caste_category: str = "general"
    age: int = 30
    name: str = "User"
    top_n: int = 8

class QuickMatchRequest(BaseModel):
    capital: float
    skills: List[str] = ["any"]
    risk_appetite: str = "medium"
    city_tier: str = "metro"

QUICK_MATCH_TABLE = {
    "street": {  # capital < 20000
        "low":    [("tea_stall","Tea Stall",15000,"95%"),("vegetable_vendor","Vegetable Cart",8000,"90%"),("pan_shop","Pan Shop",10000,"88%")],
        "medium": [("mobile_repair","Mobile Repair",18000,"78%"),("tea_stall","Tea Stall",15000,"92%")],
        "high":   [("mobile_repair","Mobile Repair",18000,"82%"),("tailoring","Tailoring",20000,"76%")],
    },
    "micro": {   # capital 20k–100k
        "low":    [("grocery","Kirana Store",50000,"88%"),("salon","Salon",80000,"82%"),("tailoring","Tailoring",25000,"90%")],
        "medium": [("salon","Salon",80000,"85%"),("grocery","Kirana Store",50000,"87%"),("bakery","Bakery",60000,"80%")],
        "high":   [("pharmacy","Medical Store",100000,"78%"),("electronics","Mobile Shop",80000,"76%"),("cafe","Cafe",90000,"74%")],
    },
    "small": {   # capital 100k–1M
        "low":    [("grocery","Supermarket",300000,"85%"),("restaurant","Restaurant",250000,"80%"),("medical_store","Medical Store",200000,"88%")],
        "medium": [("cafe","Cafe Lounge",350000,"82%"),("gym","Fitness Centre",500000,"75%"),("coaching","Coaching Centre",150000,"88%")],
        "high":   [("electronics","Electronics Store",400000,"75%"),("gym","Gym",500000,"78%"),("clinic","Clinic",500000,"80%")],
    },
    "medium": {  # capital > 1M
        "low":    [("school","School/Pre-school",1000000,"80%"),("clinic","Multi-specialty Clinic",700000,"85%")],
        "medium": [("gym","Premium Gym",800000,"78%"),("restaurant","Restaurant Chain",600000,"82%")],
        "high":   [("jewellery","Jewellery Store",1000000,"75%"),("electronics","Electronics Showroom",800000,"77%")],
    },
}

def _get_tier(capital: float) -> str:
    if capital < 20000:   return "street"
    if capital < 100000:  return "micro"
    if capital < 1000000: return "small"
    return "medium"

@router.post("/scan")
async def full_match(req: MatchRequest):
    try:
        from ai_engine.location.scanner import LocationScanner
        from ai_engine.matching.matcher import PersonBusinessMatcher, PersonProfile
        scanner = LocationScanner()
        matcher = PersonBusinessMatcher()
        profile = await scanner.scan_pincode(req.pincode)
        gaps    = scanner.identify_gaps(profile)
        person  = PersonProfile(
            name=req.name, pincode=req.pincode, capital=req.capital,
            skills=req.skills, education=req.education, language=req.language,
            has_space=req.has_space, risk_appetite=req.risk_appetite,
            is_woman=req.is_woman, caste_category=req.caste_category, age=req.age,
        )
        matches = matcher.match(person, gaps, top_n=req.top_n)
        return {
            "pincode": profile.pincode, "city": profile.city, "state": profile.state,
            "opportunity_score": profile.opportunity_score,
            "income_tier": profile.income_tier,
            "matches": [{
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
            "total_gaps_found": len(gaps),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quick")
async def quick_match(req: QuickMatchRequest):
    tier  = _get_tier(req.capital)
    risk  = req.risk_appetite if req.risk_appetite in ["low","medium","high"] else "medium"
    rows  = QUICK_MATCH_TABLE.get(tier, QUICK_MATCH_TABLE["micro"]).get(risk, [])
    return {
        "capital_tier": tier,
        "risk": risk,
        "quick_matches": [{"business_type": r[0], "display_name": r[1], "capital_needed": r[2], "success_rate": r[3]} for r in rows],
        "message": f"Based on Rs.{req.capital:,.0f} capital at {risk} risk in {req.city_tier} area",
    }

@router.get("/skills")
async def list_skills():
    from ai_engine.matching.matcher import SKILL_MAP
    return {
        "skills": [{"key": k, "businesses": v, "label": k.replace("_"," ").title()} for k, v in SKILL_MAP.items()],
    }

@router.get("/business-types")
async def list_business_types():
    from ai_engine.location.scanner import LocationScanner
    s = LocationScanner()
    return {
        "business_types": [{
            "type": biz,
            "display": biz.replace("_"," ").title(),
            "capital_needed": s.CAPITAL_NEEDED.get(biz,0),
            "monthly_revenue": s.REVENUE_ESTIMATES.get(biz,0),
        } for biz in s.BUSINESS_TYPES]
    }
