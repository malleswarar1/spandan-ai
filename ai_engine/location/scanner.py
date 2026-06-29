"""SPANDAN AI — Location Intelligence Engine"""
import asyncio
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger("spandan.location")

@dataclass
class LocationProfile:
    pincode: str
    city: str
    state: str
    lat: float
    lng: float
    population: int
    avg_income: float
    income_tier: str
    age_dominant: str
    existing_businesses: dict
    delivery_gap_score: float
    footfall_score: float
    growth_score: float
    opportunity_score: float

@dataclass
class BusinessGap:
    business_type: str
    urgency: str
    estimated_monthly_revenue: float
    min_capital_needed: float
    competition_level: str
    target_capital_tier: str
    rationale: str

class LocationScanner:

    BUSINESS_TYPES = [
        "grocery","pharmacy","salon","restaurant","cafe","gym",
        "clinic","school","coaching","hardware","clothing",
        "electronics","jewellery","mobile_repair","tailoring",
        "vegetable_vendor","tea_stall","pan_shop","medical_store",
        "bank_atm","laundry","bakery","stationery","auto_repair",
    ]

    DEMAND_RATIOS = {
        "grocery":300,"pharmacy":500,"salon":800,"restaurant":400,
        "cafe":1000,"gym":2000,"clinic":1500,"school":5000,
        "coaching":2000,"hardware":2000,"clothing":1500,
        "electronics":3000,"jewellery":5000,"mobile_repair":1000,
        "tailoring":500,"vegetable_vendor":200,"tea_stall":300,
        "pan_shop":400,"medical_store":800,"bank_atm":2000,
        "laundry":1000,"bakery":1500,"stationery":800,"auto_repair":1500,
    }

    REVENUE_ESTIMATES = {
        "grocery":120000,"pharmacy":80000,"salon":60000,
        "restaurant":150000,"cafe":100000,"gym":200000,
        "clinic":250000,"school":500000,"coaching":80000,
        "hardware":100000,"clothing":120000,"electronics":200000,
        "jewellery":300000,"mobile_repair":40000,"tailoring":30000,
        "vegetable_vendor":25000,"tea_stall":20000,"pan_shop":15000,
        "medical_store":90000,"bank_atm":0,"laundry":40000,
        "bakery":60000,"stationery":30000,"auto_repair":80000,
    }

    CAPITAL_NEEDED = {
        "vegetable_vendor":5000,"tea_stall":8000,"pan_shop":10000,
        "mobile_repair":15000,"tailoring":20000,"stationery":25000,
        "grocery":50000,"pharmacy":100000,"salon":80000,
        "laundry":50000,"bakery":60000,"coaching":30000,
        "hardware":100000,"restaurant":200000,"cafe":300000,
        "clothing":150000,"medical_store":200000,"auto_repair":100000,
        "electronics":300000,"gym":500000,"clinic":500000,
        "jewellery":500000,"school":1000000,"bank_atm":200000,
    }

    async def scan_pincode(self, pincode: str) -> LocationProfile:
        logger.info(f"Scanning: {pincode}")
        demographics, businesses, coords = await asyncio.gather(
            self._get_demographics(pincode),
            self._get_existing_businesses(pincode),
            self._get_coordinates(pincode),
        )
        lat, lng, city, state = coords
        footfall = self._calc_footfall(businesses)
        growth   = self._calc_growth(demographics)
        delivery = self._calc_delivery_gap(businesses, demographics)
        oppty    = self._calc_opportunity(demographics, businesses, footfall, growth)
        return LocationProfile(
            pincode=pincode, city=city, state=state,
            lat=lat, lng=lng,
            population=demographics.get("population", 0),
            avg_income=demographics.get("avg_income", 0),
            income_tier=self._classify_income(demographics.get("avg_income", 0)),
            age_dominant=demographics.get("age_dominant", "working"),
            existing_businesses=businesses,
            delivery_gap_score=delivery, footfall_score=footfall,
            growth_score=growth, opportunity_score=oppty,
        )

    def identify_gaps(self, profile: LocationProfile) -> list:
        gaps = []
        families = profile.population // 4
        for biz in self.BUSINESS_TYPES:
            needed   = max(1, families // self.DEMAND_RATIOS[biz])
            existing = profile.existing_businesses.get(biz, 0)
            gap      = needed - existing
            if gap <= 0:
                continue
            ratio = gap / max(needed, 1)
            if ratio >= 0.8:   urgency = "critical"
            elif ratio >= 0.5: urgency = "high"
            elif ratio >= 0.3: urgency = "medium"
            else:              urgency = "low"
            mult = {"low":0.5,"lower_mid":0.7,"mid":1.0,"upper_mid":1.4,"high":2.0}.get(profile.income_tier,1.0)
            rev  = self.REVENUE_ESTIMATES[biz] * mult
            cap  = self.CAPITAL_NEEDED[biz]
            if cap < 20000:     tier = "street"
            elif cap < 100000:  tier = "micro"
            elif cap < 1000000: tier = "small"
            else:               tier = "medium"
            gaps.append(BusinessGap(
                business_type=biz, urgency=urgency,
                estimated_monthly_revenue=round(rev),
                min_capital_needed=cap,
                competition_level=self._competition(biz, existing, needed),
                target_capital_tier=tier,
                rationale=f"{gap} {biz} units needed for {families} families in {profile.city}."
            ))
        order = {"critical":0,"high":1,"medium":2,"low":3}
        gaps.sort(key=lambda g: (order[g.urgency], -g.estimated_monthly_revenue))
        return gaps

    async def _get_demographics(self, pincode: str) -> dict:
        seed = {
            "560001":{"population":45000,"avg_income":850000,"age_dominant":"working"},
            "560037":{"population":85000,"avg_income":1200000,"age_dominant":"working"},
            "560066":{"population":120000,"avg_income":950000,"age_dominant":"family"},
            "560100":{"population":95000,"avg_income":750000,"age_dominant":"working"},
            "400001":{"population":65000,"avg_income":900000,"age_dominant":"working"},
            "110001":{"population":55000,"avg_income":700000,"age_dominant":"youth"},
            "500001":{"population":75000,"avg_income":850000,"age_dominant":"working"},
            "600001":{"population":60000,"avg_income":780000,"age_dominant":"family"},
        }
        return seed.get(pincode, {"population":50000,"avg_income":600000,"age_dominant":"working"})

    async def _get_existing_businesses(self, pincode: str) -> dict:
        if pincode == "560037":
            return {"grocery":8,"pharmacy":3,"salon":5,"restaurant":12,
                    "cafe":4,"gym":2,"clinic":3,"school":4,"coaching":6,
                    "hardware":2,"clothing":6,"mobile_repair":4,"tailoring":3,
                    "vegetable_vendor":6,"tea_stall":10,"pan_shop":8,
                    "medical_store":2,"bank_atm":5,"laundry":1,"bakery":2}
        return {biz: 0 for biz in self.BUSINESS_TYPES}

    async def _get_coordinates(self, pincode: str) -> tuple:
        coords = {
            "560001":(12.9716,77.5946,"Bangalore","Karnataka"),
            "560037":(12.9698,77.7500,"Whitefield","Karnataka"),
            "560066":(13.0358,77.5970,"Hebbal","Karnataka"),
            "560100":(12.8399,77.6770,"Electronic City","Karnataka"),
            "400001":(18.9388,72.8354,"Mumbai","Maharashtra"),
            "110001":(28.6139,77.2090,"Delhi","Delhi"),
            "600001":(13.0827,80.2707,"Chennai","Tamil Nadu"),
            "500001":(17.3850,78.4867,"Hyderabad","Telangana"),
        }
        return coords.get(pincode,(12.9716,77.5946,"Bangalore","Karnataka"))

    def _classify_income(self, i: float) -> str:
        if i < 200000:  return "low"
        if i < 500000:  return "lower_mid"
        if i < 900000:  return "mid"
        if i < 1500000: return "upper_mid"
        return "high"

    def _calc_footfall(self, b: dict) -> float:
        return min(1.0, sum(b.values()) / 50)

    def _calc_growth(self, d: dict) -> float:
        return min(1.0, d.get("avg_income", 0) / 1500000)

    def _calc_delivery_gap(self, b: dict, d: dict) -> float:
        ideal = d.get("population", 1) / 300
        return round(max(0, ideal - b.get("grocery", 0)) / max(ideal, 1), 2)

    def _calc_opportunity(self, d, b, footfall, growth) -> float:
        inc = min(1.0, d.get("avg_income", 0) / 1000000)
        pop = min(1.0, d.get("population", 0) / 100000)
        gap = max(0, 1 - sum(b.values()) / 100)
        return round((pop*0.3 + inc*0.3 + growth*0.2 + gap*0.2) * 100, 1)

    def _competition(self, biz: str, existing: int, needed: int) -> str:
        r = existing / max(needed, 1)
        if r == 0:  return "none"
        if r < 0.3: return "low"
        if r < 0.7: return "medium"
        return "high"

    async def scan_city(self, pincodes: list) -> dict:
        profiles = await asyncio.gather(*[self.scan_pincode(p) for p in pincodes])
        return {p.pincode: {"profile": p, "gaps": self.identify_gaps(p)} for p in profiles}
