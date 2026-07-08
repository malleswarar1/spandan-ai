"""SPANDAN AI — Identity & Profile Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
router = APIRouter()

class IdentityRequest(BaseModel):
    name: str
    age: int = 30
    gender: str = "male"
    education: str = "10th"
    occupation: str = "unemployed"
    pincode: str = "110001"
    state: str = "Delhi"
    district: str = ""
    languages: List[str] = ["Hindi"]
    skills: List[str] = ["any"]
    capital: float = 50000
    is_woman: bool = False
    caste_category: str = "general"
    has_space: bool = False
    risk_appetite: str = "medium"

class QuickIdentityRequest(BaseModel):
    capital: float
    skills: List[str] = ["any"]
    is_woman: bool = False
    caste_category: str = "general"
    education: str = "10th"
    age: int = 30

@router.post("/analyse")
async def analyse_identity(req: IdentityRequest):
    try:
        from ai_engine.identity.profiler import IdentityProfiler, IdentityProfile
        profiler = IdentityProfiler()
        identity = IdentityProfile(
            person_name=req.name,
            age=req.age,
            gender=req.gender,
            education=req.education,
            occupation=req.occupation,
            pincode=req.pincode,
            state=req.state,
            district=req.district or req.state,
            languages=req.languages,
            skills=req.skills,
            capital=req.capital,
            is_woman=req.is_woman,
            caste_category=req.caste_category,
            has_space=req.has_space,
            risk_appetite=req.risk_appetite,
        )
        result = profiler.build_profile(identity)
        return {
            "name": req.name,
            "opportunity_score": result.opportunity_score,
            "economic_tier": result.economic_tier,
            "entrepreneurship_readiness": result.entrepreneurship_readiness,
            "monthly_income_potential": result.monthly_income_potential,
            "digital_literacy_score": result.digital_literacy_score,
            "summary": result.summary,
            "hindi_summary": result.hindi_summary,
            "recommended_paths": [
                {
                    "path_name": p.path_name,
                    "description": p.description,
                    "capital_needed": p.capital_needed,
                    "timeline_months": p.timeline_months,
                    "expected_monthly_income": p.expected_monthly_income,
                    "first_steps": p.first_steps,
                    "risks": p.risks,
                    "success_rate": p.success_rate,
                } for p in result.recommended_paths
            ],
            "government_eligibilities": [
                {
                    "scheme_id": g.scheme_id,
                    "scheme_name": g.scheme_name,
                    "ministry": g.ministry,
                    "max_benefit": g.max_benefit,
                    "eligible": g.eligible,
                    "reason": g.reason,
                    "action_required": g.action_required,
                    "priority": g.priority,
                } for g in result.government_eligibilities
            ],
            "skill_gaps": [
                {
                    "skill_name": g.skill_name,
                    "importance": g.importance,
                    "learning_time_days": g.learning_time_days,
                    "free_resource": g.free_resource,
                    "government_course": g.government_course,
                    "expected_income_boost": g.expected_income_boost,
                } for g in result.skill_gaps
            ],
            "strengths": result.strengths,
            "challenges": result.challenges,
            "immediate_actions": result.immediate_actions,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quick-assess")
async def quick_assess(req: QuickIdentityRequest):
    """Fast eligibility + top paths check without full location scan"""
    from ai_engine.identity.profiler import IdentityProfiler, IdentityProfile
    profiler = IdentityProfiler()
    identity = IdentityProfile(
        person_name="User",
        age=req.age,
        gender="other",
        education=req.education,
        occupation="",
        pincode="110001",
        state="India",
        district="",
        languages=["Hindi"],
        skills=req.skills,
        capital=req.capital,
        is_woman=req.is_woman,
        caste_category=req.caste_category,
        has_space=False,
        risk_appetite="medium",
    )
    result = profiler.build_profile(identity)
    immediate = [g for g in result.government_eligibilities if g.priority == "immediate"]
    return {
        "opportunity_score": result.opportunity_score,
        "economic_tier": result.economic_tier,
        "monthly_income_potential": result.monthly_income_potential,
        "top_path": {
            "name": result.recommended_paths[0].path_name,
            "income": result.recommended_paths[0].expected_monthly_income,
            "capital": result.recommended_paths[0].capital_needed,
        } if result.recommended_paths else None,
        "immediate_schemes": [{"name": g.scheme_name, "benefit": g.max_benefit} for g in immediate],
        "immediate_actions": result.immediate_actions[:3],
    }

@router.get("/education-levels")
async def education_levels():
    from ai_engine.identity.profiler import EDUCATION_LEVELS
    return {
        "levels": [{"key": k, "level": v, "label": k.replace("_"," ").title()} for k, v in EDUCATION_LEVELS.items()]
    }

@router.get("/skills-catalogue")
async def skills_catalogue():
    from ai_engine.matching.matcher import SKILL_MAP
    from ai_engine.identity.profiler import SKILL_COURSES
    result = []
    for skill, businesses in SKILL_MAP.items():
        course_info = SKILL_COURSES.get(skill, {})
        result.append({
            "skill": skill,
            "label": skill.replace("_"," ").title(),
            "businesses": businesses,
            "free_course": course_info.get("resource","YouTube tutorials"),
            "govt_course": course_info.get("course","PMKVY — check smarth.nsdcindia.org"),
            "training_days": course_info.get("days", 30),
        })
    return {"skills": result}

@router.get("/opportunity-calculator")
async def opportunity_calculator(
    capital: float = 50000,
    skills: str = "any",
    age: int = 30,
    is_woman: bool = False,
    caste_category: str = "general",
):
    """Quick URL-param based calculator"""
    from ai_engine.identity.profiler import IdentityProfiler, IdentityProfile
    profiler = IdentityProfiler()
    identity = IdentityProfile(
        person_name="User",
        age=age,
        gender="female" if is_woman else "male",
        education="10th",
        occupation="",
        pincode="110001",
        state="India",
        district="",
        languages=["Hindi"],
        skills=[s.strip() for s in skills.split(",")],
        capital=capital,
        is_woman=is_woman,
        caste_category=caste_category,
        has_space=False,
        risk_appetite="medium",
    )
    result = profiler.build_profile(identity)
    return {
        "opportunity_score": result.opportunity_score,
        "monthly_income_potential": result.monthly_income_potential,
        "economic_tier": result.economic_tier,
        "readiness": result.entrepreneurship_readiness,
        "top_path": result.recommended_paths[0].path_name if result.recommended_paths else None,
    }
