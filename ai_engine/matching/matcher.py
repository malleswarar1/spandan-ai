"""SPANDAN AI — Person to Business Matcher"""
from dataclasses import dataclass
import logging

logger = logging.getLogger("spandan.matching")

@dataclass
class PersonProfile:
    name: str
    pincode: str
    capital: float
    skills: list
    education: str
    language: str
    has_space: bool
    risk_appetite: str
    is_woman: bool
    caste_category: str
    age: int

@dataclass
class MatchResult:
    business_type: str
    match_score: float
    monthly_revenue_estimate: float
    capital_needed: float
    capital_gap: float
    funding_schemes: list
    setup_steps: list
    location_advice: str
    success_probability: str

SKILL_MAP = {
    "cooking":  ["restaurant","cafe","bakery","tea_stall"],
    "tailoring":["tailoring","clothing"],
    "selling":  ["grocery","vegetable_vendor","clothing"],
    "repair":   ["mobile_repair","auto_repair"],
    "teaching": ["coaching","school"],
    "beauty":   ["salon"],
    "health":   ["clinic","pharmacy","medical_store"],
    "any":      ["tea_stall","pan_shop","vegetable_vendor","mobile_repair"],
}

class PersonBusinessMatcher:

    def match(self, person: PersonProfile, gaps: list, top_n: int = 5) -> list:
        results = []
        for gap in gaps:
            score = self._score(person, gap)
            if score < 0.2:
                continue
            cap_gap = max(0, gap.min_capital_needed - person.capital)
            results.append(MatchResult(
                business_type=gap.business_type,
                match_score=round(score, 2),
                monthly_revenue_estimate=gap.estimated_monthly_revenue,
                capital_needed=gap.min_capital_needed,
                capital_gap=cap_gap,
                funding_schemes=self._schemes(person, cap_gap),
                setup_steps=self._steps(gap.business_type),
                location_advice=self._advice(gap.business_type, person),
                success_probability=self._success(score, gap),
            ))
        results.sort(key=lambda r: r.match_score, reverse=True)
        return results[:top_n]

    def _score(self, person: PersonProfile, gap) -> float:
        score = 0.0
        ratio = person.capital / max(gap.min_capital_needed, 1)
        if ratio >= 1.0:   score += 0.4
        elif ratio >= 0.5: score += 0.25
        elif ratio >= 0.3: score += 0.1
        matched = [s for s in person.skills if gap.business_type in SKILL_MAP.get(s, [])]
        score += min(0.3, len(matched) * 0.15)
        score += {"critical":0.2,"high":0.15,"medium":0.1,"low":0.05}.get(gap.urgency, 0.05)
        score += {"high":0.1,"medium":0.07,"low":0.05}.get(person.risk_appetite, 0.05)
        return min(1.0, score)

    def _schemes(self, person: PersonProfile, cap_gap: float) -> list:
        if cap_gap <= 0:
            return ["Self-funded — no loan needed"]
        schemes = []
        if cap_gap <= 50000:
            schemes.append("PM SVANidhi (up to Rs.50,000 — street vendors)")
            schemes.append("MUDRA Shishu (up to Rs.50,000 — no collateral)")
        elif cap_gap <= 500000:
            schemes.append("MUDRA Kishor (up to Rs.5 lakh — no collateral)")
        else:
            schemes.append("MUDRA Tarun (up to Rs.10 lakh — no collateral)")
        schemes.append("PMEGP (up to Rs.25 lakh — 15-35% subsidy)")
        if person.is_woman:
            schemes.append("Mahila Udyam Nidhi (soft loan for women)")
        if person.caste_category in ["sc","st"]:
            schemes.append("Stand-Up India SC/ST (up to Rs.1 crore)")
        return schemes[:4]

    def _steps(self, biz: str) -> list:
        specific = {
            "tea_stall":        ["Find spot near bus stop or office gate","Buy stove + kettle + cups (Rs.5,000-8,000)","Source milk + tea locally","Target 50 cups/day"],
            "vegetable_vendor": ["Find nearest APMC wholesale mandi","Buy push-cart (Rs.2,000-5,000)","Start with 5-7 common vegetables","Build customer route within 500m"],
            "grocery":          ["Register shop with municipality","Source from wholesale market","Install QR payment (free)","Stock top 100 fast-moving items first"],
            "salon":            ["Complete NSDC beautician course (free)","Buy basic equipment (Rs.30,000-50,000)","Register with municipality","List on UrbanClap for home service"],
            "pharmacy":         ["Get D.Pharma certificate","Apply for drug license","Source from authorized distributor","Keep 500 essential medicines in stock"],
            "cafe":             ["Find location near office or college","Get FSSAI license (free online)","Buy coffee machine + furniture","Offer WiFi as differentiator"],
        }
        base = specific.get(biz, [
            f"Research top {biz.replace('_',' ')} suppliers in your area",
            "Visit 3 similar businesses to learn operations",
            "Create 6-month revenue plan",
            "Apply for MUDRA loan",
        ])
        return base + ["Register free on udyamregistration.gov.in","Open current bank account"]

    def _advice(self, biz: str, person: PersonProfile) -> str:
        return {
            "tea_stall":        "Near bus stops, railway stations, office gates. Morning + evening shifts.",
            "vegetable_vendor": "Residential streets near apartments. Early morning 6-9 AM peak.",
            "grocery":          "Ground floor corner unit near residential cluster. 200m from competitor.",
            "pharmacy":         "Near clinic or hospital. Ground floor with parking.",
            "salon":            "Near residential entry, not main road. Women prefer quiet lanes.",
            "cafe":             "Near offices, colleges, coworking. WiFi is key differentiator.",
            "gym":              "Near residential cluster. First floor reduces rent cost.",
            "restaurant":       "Near offices for lunch crowd. Evening near residential areas.",
        }.get(biz, f"Choose high-footfall area near target customers in {person.pincode}.")

    def _success(self, score: float, gap) -> str:
        if score >= 0.8 and gap.urgency in ["critical","high"]: return "Very High (85%+)"
        if score >= 0.6: return "High (70-85%)"
        if score >= 0.4: return "Medium (50-70%)"
        return "Moderate (40-55%)"
