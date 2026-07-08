"""SPANDAN AI — Funding Schemes Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
router = APIRouter()

SCHEMES = [
    {
        "id": "mudra_shishu",
        "name": "MUDRA Shishu Loan",
        "ministry": "Ministry of Finance / MUDRA",
        "max_amount": 50000,
        "min_amount": 1000,
        "interest_rate": "8-12%",
        "collateral": False,
        "subsidy_percent": 0,
        "target": ["all"],
        "business_types": ["tea_stall","vegetable_vendor","pan_shop","tailoring","mobile_repair","salon","grocery"],
        "eligibility": ["Non-farm income generating activities","Age 18-65","Micro/small enterprise"],
        "documents": ["Aadhaar","PAN","Bank account passbook","Business proof","2 passport photos"],
        "apply_at": "Any nationalized bank, NBFC-MFI, or Udyami Mitra portal",
        "apply_url": "https://udyamimitra.in",
        "processing_days": 7,
        "description": "For micro enterprises needing up to Rs.50,000 to start or expand. Zero collateral needed.",
        "hindi_name": "मुद्रा शिशु ऋण",
        "tags": ["no_collateral","street_vendor","micro"],
    },
    {
        "id": "mudra_kishor",
        "name": "MUDRA Kishor Loan",
        "ministry": "Ministry of Finance / MUDRA",
        "max_amount": 500000,
        "min_amount": 50001,
        "interest_rate": "8-12%",
        "collateral": False,
        "subsidy_percent": 0,
        "target": ["all"],
        "business_types": ["grocery","pharmacy","salon","restaurant","cafe","hardware","clothing","bakery","stationery","laundry","auto_repair"],
        "eligibility": ["Existing micro/small business","Age 18-65","Min 6 months business vintage"],
        "documents": ["Aadhaar","PAN","Business registration","GST certificate","Bank statement 6 months","2 passport photos"],
        "apply_at": "Any scheduled commercial bank or MUDRA-registered NBFC",
        "apply_url": "https://udyamimitra.in",
        "processing_days": 14,
        "description": "For established micro businesses needing Rs.50,001–5 lakh for growth. No collateral required.",
        "hindi_name": "मुद्रा किशोर ऋण",
        "tags": ["no_collateral","micro_shop","growth"],
    },
    {
        "id": "mudra_tarun",
        "name": "MUDRA Tarun Loan",
        "ministry": "Ministry of Finance / MUDRA",
        "max_amount": 1000000,
        "min_amount": 500001,
        "interest_rate": "9-14%",
        "collateral": True,
        "subsidy_percent": 0,
        "target": ["all"],
        "business_types": ["restaurant","cafe","gym","clinic","school","coaching","electronics","medical_store","auto_repair"],
        "eligibility": ["Established small business","Age 21-65","Min 2 years business history","Clean credit history"],
        "documents": ["Aadhaar","PAN","Business registration","GST","Bank statement 12 months","ITR 2 years","Property document"],
        "apply_at": "Scheduled commercial banks with MUDRA license",
        "apply_url": "https://udyamimitra.in",
        "processing_days": 21,
        "description": "For growing businesses needing Rs.5–10 lakh. Light collateral may be needed.",
        "hindi_name": "मुद्रा तरुण ऋण",
        "tags": ["small_business","growth","collateral"],
    },
    {
        "id": "pm_svanidhi",
        "name": "PM SVANidhi",
        "ministry": "Ministry of Housing & Urban Affairs",
        "max_amount": 50000,
        "min_amount": 10000,
        "interest_rate": "7%",
        "collateral": False,
        "subsidy_percent": 7,
        "target": ["street_vendor"],
        "business_types": ["tea_stall","vegetable_vendor","pan_shop","mobile_repair"],
        "eligibility": ["Urban street vendor","Vending certificate","Age 18-65","Not defaulter"],
        "documents": ["Aadhaar","Vending certificate / Letter of Recommendation from ULB","Bank account"],
        "apply_at": "Common Service Centre (CSC) or pmsvanidhi.mohua.gov.in",
        "apply_url": "https://pmsvanidhi.mohua.gov.in",
        "processing_days": 5,
        "description": "Special scheme for urban street vendors. Start with Rs.10,000, repay and get Rs.20,000, then Rs.50,000. Cashback on digital payments.",
        "hindi_name": "पीएम स्वनिधि",
        "tags": ["street_vendor","digital_cashback","no_collateral","fast"],
    },
    {
        "id": "pmegp",
        "name": "PMEGP — PM Employment Generation Programme",
        "ministry": "Ministry of MSME / KVIC",
        "max_amount": 2500000,
        "min_amount": 100000,
        "interest_rate": "11-15%",
        "collateral": False,
        "subsidy_percent": 25,
        "target": ["all"],
        "business_types": ["grocery","pharmacy","salon","restaurant","cafe","gym","clinic","school","coaching","hardware","clothing","electronics","jewellery","laundry","bakery","auto_repair"],
        "eligibility": ["Age 18+","Min 8th pass for projects > Rs.10 lakh","No existing enterprise","Not availed subsidy before"],
        "documents": ["Aadhaar","PAN","Class 8 certificate","Project report","Bank account","Caste certificate (if applicable)"],
        "apply_at": "KVIC / KVIB / DIC offices, or kviconline.gov.in",
        "apply_url": "https://www.kviconline.gov.in/pmegpeportal",
        "processing_days": 45,
        "description": "Up to Rs.25 lakh for manufacturing, Rs.10 lakh for service businesses. Govt subsidizes 15–35% upfront.",
        "subsidy_detail": {"general_urban": "15%", "general_rural": "25%", "sc_st_obc_women_minorities_ner": "35%"},
        "hindi_name": "पीएमईजीपी",
        "tags": ["subsidy","no_collateral","small_medium"],
    },
    {
        "id": "stand_up_india",
        "name": "Stand-Up India",
        "ministry": "Ministry of Finance",
        "max_amount": 10000000,
        "min_amount": 1000000,
        "interest_rate": "Base Rate + 3% + Tenor Premium",
        "collateral": True,
        "subsidy_percent": 0,
        "target": ["sc","st","women"],
        "business_types": ["school","clinic","gym","electronics","jewellery","grocery"],
        "eligibility": ["SC/ST or Woman entrepreneur","Age 18+","Greenfield enterprise","Min 51% SC/ST/Women ownership"],
        "documents": ["Aadhaar","PAN","Caste/gender certificate","Project report","Bank account","Property document"],
        "apply_at": "standupmitra.in or any scheduled commercial bank",
        "apply_url": "https://www.standupmitra.in",
        "processing_days": 30,
        "description": "For SC/ST and women entrepreneurs to set up greenfield enterprises. Loans Rs.10 lakh–1 crore.",
        "hindi_name": "स्टैंड-अप इंडिया",
        "tags": ["sc_st","women","large_loan","greenfield"],
    },
    {
        "id": "mahila_udyam_nidhi",
        "name": "Mahila Udyam Nidhi",
        "ministry": "SIDBI / Punjab National Bank",
        "max_amount": 1000000,
        "min_amount": 10000,
        "interest_rate": "10-12%",
        "collateral": False,
        "subsidy_percent": 0,
        "target": ["women"],
        "business_types": ["salon","tailoring","bakery","grocery","clothing","pharmacy","coaching"],
        "eligibility": ["Woman entrepreneur","Age 18-55","Viable business plan","Not defaulter"],
        "documents": ["Aadhaar","PAN","Business plan","Bank account","Proof of ownership"],
        "apply_at": "SIDBI or select nationalized banks",
        "apply_url": "https://www.sidbi.in",
        "processing_days": 21,
        "description": "Soft loan for women entrepreneurs setting up small enterprises. Up to Rs.10 lakh with concessional interest.",
        "hindi_name": "महिला उद्यम निधि",
        "tags": ["women","soft_loan","micro_small"],
    },
    {
        "id": "cgfmu",
        "name": "CGFMU — Credit Guarantee for Micro Units",
        "ministry": "Ministry of Finance / NCGTC",
        "max_amount": 2000000,
        "min_amount": 50000,
        "interest_rate": "Varies by bank",
        "collateral": False,
        "subsidy_percent": 0,
        "target": ["all"],
        "business_types": ["grocery","pharmacy","salon","restaurant","coaching","hardware"],
        "eligibility": ["MUDRA registered borrower","Viable micro business","No existing default"],
        "documents": ["MUDRA loan documents","Business registration","Aadhaar","PAN"],
        "apply_at": "Via MUDRA lending institutions",
        "apply_url": "https://www.mudra.org.in",
        "processing_days": 10,
        "description": "Government provides credit guarantee so banks lend without collateral to micro units. Works alongside MUDRA loans.",
        "hindi_name": "सीजीएफएमयू",
        "tags": ["no_collateral","guarantee","micro"],
    },
    {
        "id": "nsic_marketing",
        "name": "NSIC Marketing Support",
        "ministry": "Ministry of MSME / NSIC",
        "max_amount": 500000,
        "min_amount": 10000,
        "interest_rate": "8%",
        "collateral": False,
        "subsidy_percent": 0,
        "target": ["all"],
        "business_types": ["clothing","electronics","hardware","stationery","bakery"],
        "eligibility": ["MSME registered","Manufacturing or trading unit","Age 18+"],
        "documents": ["Udyam registration","Bank account","Trade license","Aadhaar","PAN"],
        "apply_at": "NSIC branches or nsic.co.in",
        "apply_url": "https://www.nsic.co.in",
        "processing_days": 15,
        "description": "Marketing, raw material, and technology support for small businesses. Helps get government tenders.",
        "hindi_name": "एनएसआईसी मार्केटिंग सहायता",
        "tags": ["msme","marketing","tender"],
    },
    {
        "id": "wdc_dena",
        "name": "Women Development Corporation Loan",
        "ministry": "State Governments",
        "max_amount": 200000,
        "min_amount": 10000,
        "interest_rate": "4-8%",
        "collateral": False,
        "subsidy_percent": 10,
        "target": ["women"],
        "business_types": ["salon","tailoring","grocery","bakery","coaching","clothing"],
        "eligibility": ["Woman","Age 18-55","Below poverty line / low income","State resident"],
        "documents": ["Aadhaar","BPL card or income certificate","Bank account","Business plan","2 photos"],
        "apply_at": "State Women & Child Development Department office",
        "apply_url": "State government portal (varies by state)",
        "processing_days": 30,
        "description": "State-level soft loans for women from low-income households. Interest rates as low as 4%.",
        "hindi_name": "महिला विकास निगम ऋण",
        "tags": ["women","state_scheme","low_interest"],
    },
    {
        "id": "pm_fme",
        "name": "PM Formalization of Micro Food Enterprises",
        "ministry": "Ministry of Food Processing Industries",
        "max_amount": 1000000,
        "min_amount": 50000,
        "interest_rate": "Subsidized (35% capital subsidy)",
        "collateral": False,
        "subsidy_percent": 35,
        "target": ["all"],
        "business_types": ["restaurant","cafe","bakery","tea_stall","grocery"],
        "eligibility": ["Food processing/selling enterprise","Udyam registered","FSSAI licensed or willing to register"],
        "documents": ["Aadhaar","PAN","Udyam registration","FSSAI registration","Bank account","Project report"],
        "apply_at": "pmfme.mofpi.gov.in",
        "apply_url": "https://pmfme.mofpi.gov.in",
        "processing_days": 45,
        "description": "35% capital subsidy (up to Rs.10 lakh) for micro food enterprises. Helps formalize street food, home kitchen, small eateries.",
        "hindi_name": "पीएम एफएमई",
        "tags": ["food","subsidy","formalization"],
    },
    {
        "id": "skill_india_loan",
        "name": "Skill India Vocational Training Loan",
        "ministry": "Ministry of Skill Development",
        "max_amount": 150000,
        "min_amount": 5000,
        "interest_rate": "6% (subsidized)",
        "collateral": False,
        "subsidy_percent": 0,
        "target": ["youth","all"],
        "business_types": ["mobile_repair","auto_repair","salon","tailoring","coaching"],
        "eligibility": ["Age 15-45","Pursuing NSDC/PMKVY course","Indian citizen"],
        "documents": ["Aadhaar","Course enrollment proof","Bank account","Age proof"],
        "apply_at": "NSDC / PMKVY training centre",
        "apply_url": "https://www.skillindiadigital.gov.in",
        "processing_days": 7,
        "description": "Low-interest loans to cover skill training costs. PMKVY courses are often free + stipend. This covers tools and equipment after training.",
        "hindi_name": "स्किल इंडिया ऋण",
        "tags": ["skill_training","youth","low_interest"],
    },
]

class FundingSearchRequest(BaseModel):
    capital_gap: float
    is_woman: bool = False
    caste_category: str = "general"
    business_type: Optional[str] = None
    state: Optional[str] = None

@router.get("/schemes")
async def all_schemes():
    return {"schemes": SCHEMES, "total": len(SCHEMES)}

@router.get("/scheme/{scheme_id}")
async def get_scheme(scheme_id: str):
    scheme = next((s for s in SCHEMES if s["id"] == scheme_id), None)
    if not scheme:
        raise HTTPException(status_code=404, detail=f"Scheme {scheme_id} not found")
    return scheme

@router.post("/find")
async def find_schemes(req: FundingSearchRequest):
    matched = []
    for s in SCHEMES:
        if s["max_amount"] < req.capital_gap * 0.5:
            continue
        target = s.get("target", [])
        if "all" not in target:
            if req.is_woman and "women" not in target:
                pass
            elif req.caste_category in ["sc","st"] and "sc" not in target and "st" not in target:
                if not req.is_woman:
                    continue
        if req.business_type and s.get("business_types"):
            if req.business_type not in s["business_types"]:
                continue
        score = 0
        if req.capital_gap <= s["max_amount"]: score += 30
        if req.is_woman and "women" in target: score += 25
        if req.caste_category in ["sc","st"] and ("sc" in target or "st" in target): score += 25
        if s.get("subsidy_percent", 0) > 0: score += 20
        if not s.get("collateral", True): score += 15
        matched.append({**s, "relevance_score": score})
    matched.sort(key=lambda x: -x["relevance_score"])
    return {
        "capital_gap": req.capital_gap,
        "matched_schemes": matched[:6],
        "total_found": len(matched),
        "tip": "Apply for MUDRA first — it's fastest and has widest coverage.",
    }

@router.get("/calculator/{scheme_id}")
async def emi_calculator(scheme_id: str, amount: float, tenure_months: int = 36):
    scheme = next((s for s in SCHEMES if s["id"] == scheme_id), None)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    rate_str = scheme["interest_rate"].split("-")[0].replace("%","").strip()
    try:
        annual_rate = float(rate_str) / 100
    except Exception:
        annual_rate = 0.10
    monthly_rate = annual_rate / 12
    if monthly_rate > 0:
        emi = amount * monthly_rate * (1 + monthly_rate)**tenure_months / ((1 + monthly_rate)**tenure_months - 1)
    else:
        emi = amount / tenure_months
    total_payment = emi * tenure_months
    total_interest = total_payment - amount
    subsidy_amount = amount * scheme.get("subsidy_percent", 0) / 100
    return {
        "scheme": scheme["name"],
        "loan_amount": amount,
        "tenure_months": tenure_months,
        "monthly_emi": round(emi, 0),
        "total_payment": round(total_payment, 0),
        "total_interest": round(total_interest, 0),
        "subsidy_amount": round(subsidy_amount, 0),
        "effective_cost": round(total_payment - subsidy_amount, 0),
        "daily_repayment": round(emi / 30, 0),
    }
