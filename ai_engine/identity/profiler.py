"""
SPANDAN AI — Identity & Opportunity Profiler

Builds a complete opportunity profile for a person based on their
demographics, education, skills, location, and financial capacity.
Identifies personalized opportunities, government eligibilities, and
skill gaps with specific action plans.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("spandan.identity")

@dataclass
class SkillGap:
    skill_name: str
    importance: str         # critical / high / medium
    learning_time_days: int
    free_resource: str
    government_course: str
    expected_income_boost: str

@dataclass
class GovernmentEligibility:
    scheme_id: str
    scheme_name: str
    ministry: str
    max_benefit: str
    eligible: bool
    reason: str
    action_required: str
    priority: str           # immediate / medium / low

@dataclass
class CareerPath:
    path_name: str
    description: str
    capital_needed: float
    timeline_months: int
    expected_monthly_income: float
    first_steps: List[str]
    risks: List[str]
    success_rate: str

@dataclass
class IdentityProfile:
    person_name: str
    age: int
    gender: str
    education: str
    occupation: str
    pincode: str
    state: str
    district: str
    languages: List[str]
    skills: List[str]
    capital: float
    is_woman: bool
    caste_category: str
    has_space: bool
    risk_appetite: str

@dataclass
class OpportunityProfile:
    identity: IdentityProfile
    opportunity_score: float
    economic_tier: str
    entrepreneurship_readiness: str
    recommended_paths: List[CareerPath]
    government_eligibilities: List[GovernmentEligibility]
    skill_gaps: List[SkillGap]
    strengths: List[str]
    challenges: List[str]
    immediate_actions: List[str]
    monthly_income_potential: float
    digital_literacy_score: float
    summary: str
    hindi_summary: str


EDUCATION_LEVELS = {
    "no_schooling":  0,
    "primary":       1,
    "5th":           2,
    "8th":           3,
    "10th":          4,
    "12th":          5,
    "diploma":       6,
    "graduate":      7,
    "post_graduate": 8,
    "professional":  9,
}

SKILL_COURSES = {
    "cooking":      {"course": "PMKVY Food Processing", "days": 30, "resource": "YouTube: Chef Ranveer Brar basics"},
    "tailoring":    {"course": "NSDC Apparel Skills", "days": 45, "resource": "YouTube: Sewing Tutorials India"},
    "beauty":       {"course": "NSDC Beauty & Wellness", "days": 60, "resource": "YouTube: Meribindiya tutorials"},
    "mobile_repair":{"course": "NSDC Electronics", "days": 90, "resource": "YouTube: MobileSentrix India"},
    "computers":    {"course": "PMKVY IT", "days": 60, "resource": "Google Digital Garage (free)"},
    "english":      {"course": "PMKVY English Speaking", "days": 30, "resource": "BBC Learning English app (free)"},
    "accounting":   {"course": "Tally Operator Course", "days": 45, "resource": "Tally Education YouTube"},
    "driving":      {"course": "Commercial Vehicle Driving", "days": 30, "resource": "Local driving school"},
    "selling":      {"course": "Digital Marketing NSDC", "days": 30, "resource": "Google Skillshop (free)"},
    "farming":      {"course": "KVK Agriculture Training", "days": 60, "resource": "ICAR YouTube channel"},
    "plumbing":     {"course": "NSDC Construction", "days": 60, "resource": "YouTube: Plumbing tutorials"},
    "electrical":   {"course": "ITI Electrician", "days": 180, "resource": "YouTube: Electrician tutorial"},
    "health_care":  {"course": "NSDC Domestic Nursing Aide", "days": 90, "resource": "NHM training programmes"},
}

class IdentityProfiler:

    def build_profile(self, identity: IdentityProfile) -> OpportunityProfile:
        opp_score   = self._calc_opportunity_score(identity)
        econ_tier   = self._economic_tier(identity.capital)
        readiness   = self._entrepreneurship_readiness(identity)
        paths       = self._recommend_paths(identity, opp_score)
        eligibility = self._check_government_eligibility(identity)
        gaps        = self._identify_skill_gaps(identity)
        strengths   = self._identify_strengths(identity)
        challenges  = self._identify_challenges(identity)
        actions     = self._immediate_actions(identity, paths)
        income_pot  = self._income_potential(identity)
        digital_score = self._digital_literacy_score(identity)
        summary     = self._generate_summary(identity, opp_score, paths)
        hindi_sum   = self._generate_hindi_summary(identity, opp_score)

        return OpportunityProfile(
            identity=identity,
            opportunity_score=opp_score,
            economic_tier=econ_tier,
            entrepreneurship_readiness=readiness,
            recommended_paths=paths,
            government_eligibilities=eligibility,
            skill_gaps=gaps,
            strengths=strengths,
            challenges=challenges,
            immediate_actions=actions,
            monthly_income_potential=income_pot,
            digital_literacy_score=digital_score,
            summary=summary,
            hindi_summary=hindi_sum,
        )

    def _calc_opportunity_score(self, p: IdentityProfile) -> float:
        score = 0.0
        edu_level = EDUCATION_LEVELS.get(p.education, 4)
        score += min(25, edu_level * 3)
        score += min(20, len(p.skills) * 4)
        if p.capital >= 100000:  score += 20
        elif p.capital >= 50000: score += 15
        elif p.capital >= 20000: score += 10
        elif p.capital >= 5000:  score += 5
        age_score = 0
        if 22 <= p.age <= 35:    age_score = 15
        elif 35 < p.age <= 50:   age_score = 12
        elif p.age < 22:         age_score = 10
        else:                     age_score = 7
        score += age_score
        risk_bonus = {"high": 10, "medium": 7, "low": 5}.get(p.risk_appetite, 5)
        score += risk_bonus
        if p.is_woman:           score += 5
        if p.has_space:          score += 5
        return round(min(100, score), 1)

    def _economic_tier(self, capital: float) -> str:
        if capital < 10000:   return "street_vendor"
        if capital < 50000:   return "micro_entrepreneur"
        if capital < 200000:  return "small_business"
        if capital < 1000000: return "sme_owner"
        return "medium_enterprise"

    def _entrepreneurship_readiness(self, p: IdentityProfile) -> str:
        edu = EDUCATION_LEVELS.get(p.education, 4)
        score = 0
        if edu >= 4:         score += 2
        if len(p.skills) >= 2: score += 2
        if p.capital >= 20000: score += 2
        if p.risk_appetite == "high": score += 2
        elif p.risk_appetite == "medium": score += 1
        if 22 <= p.age <= 45: score += 2
        if score >= 8:  return "High — Ready to Start"
        if score >= 5:  return "Medium — Some preparation needed"
        if score >= 3:  return "Low — Build foundations first"
        return "Nascent — Begin with skill building"

    def _recommend_paths(self, p: IdentityProfile, score: float) -> List[CareerPath]:
        paths = []
        capital = p.capital
        skills  = [s.lower() for s in p.skills]
        edu     = EDUCATION_LEVELS.get(p.education, 4)

        if capital < 15000:
            paths.append(CareerPath(
                path_name="Street Vending — Vegetable or Tea",
                description="Start a mobile tea stall or vegetable cart near residential areas. Immediate income.",
                capital_needed=8000,
                timeline_months=1,
                expected_monthly_income=18000,
                first_steps=["Get PM SVANidhi loan (Rs.10,000, free)", "Buy cart + equipment", "Identify morning route"],
                risks=["Weather disruption", "Municipal enforcement", "Competition from existing vendors"],
                success_rate="88%",
            ))

        if "cooking" in skills or "any" in skills:
            paths.append(CareerPath(
                path_name="Home Kitchen / Tiffin Service",
                description="Cook and deliver 20-50 tiffins daily. 0 rent, high margin. Scale to cloud kitchen.",
                capital_needed=15000,
                timeline_months=2,
                expected_monthly_income=25000,
                first_steps=["Register on Zomato/Swiggy Home Chef", "Get FSSAI registration (free)", "Start with 10 daily orders via WhatsApp"],
                risks=["Consistency required", "Food safety compliance", "Delivery logistics"],
                success_rate="75%",
            ))

        if "tailoring" in skills:
            paths.append(CareerPath(
                path_name="Tailoring Shop / Boutique",
                description="Alterations, custom stitching from home or small space. Ladies tailoring in demand.",
                capital_needed=20000,
                timeline_months=1,
                expected_monthly_income=22000,
                first_steps=["Buy sewing machine (Rs.8,000-15,000)", "List on Urban Company", "Put up board in apartment complex"],
                risks=["Seasonal demand fluctuation", "Competition with readymade", "Skill standardization"],
                success_rate="82%",
            ))

        if "beauty" in skills or "any" in skills:
            paths.append(CareerPath(
                path_name="Home Salon / Beauty Services",
                description="Offer at-home beauty services. Zero rent, flexible hours. Grow to shop.",
                capital_needed=25000,
                timeline_months=2,
                expected_monthly_income=30000,
                first_steps=["Complete NSDC Beauty course (free)", "Buy starter kit", "List on Urban Company", "WhatsApp business catalog"],
                risks=["Trust building with new clients", "Skin/allergy liability", "Tools sterilization"],
                success_rate="80%",
            ))

        if capital >= 30000 and "mobile_repair" in skills:
            paths.append(CareerPath(
                path_name="Mobile Repair + Accessories Shop",
                description="High-demand, low-competition in smaller areas. Accessories = bonus passive income.",
                capital_needed=35000,
                timeline_months=2,
                expected_monthly_income=40000,
                first_steps=["NSDC mobile repair course if needed", "Rent small kiosk near market", "Source parts + accessories"],
                risks=["High-end board-level repairs need skill", "Screen replacement tools cost", "Fake parts quality"],
                success_rate="78%",
            ))

        if capital >= 50000:
            paths.append(CareerPath(
                path_name="Kirana / Grocery Store",
                description="India's most reliable micro business. Steady daily income, builds community loyalty.",
                capital_needed=60000,
                timeline_months=2,
                expected_monthly_income=55000,
                first_steps=["Find ground-floor space near residential area", "Apply MUDRA Shishu loan", "Register on Udyam portal (free)", "Source from nearest wholesale market"],
                risks=["Inventory management", "Credit to known customers", "Competition from Blinkit/Swiggy"],
                success_rate="87%",
            ))

        if capital >= 100000 and "teaching" in skills:
            paths.append(CareerPath(
                path_name="Home Tuition → Coaching Centre",
                description="Start with 10 home students, then open centre. Education is recession-proof.",
                capital_needed=50000,
                timeline_months=3,
                expected_monthly_income=70000,
                first_steps=["Identify subject expertise", "Register with Class Up or Vedantu", "Start online batches + physical centre"],
                risks=["Teacher availability for scaling", "Season-dependent (not year-round)", "Competitive in cities"],
                success_rate="85%",
            ))

        if capital >= 200000:
            paths.append(CareerPath(
                path_name="Medical Store / Pharmacy",
                description="Highly regulated but extremely stable. Near hospitals = guaranteed footfall.",
                capital_needed=200000,
                timeline_months=4,
                expected_monthly_income=90000,
                first_steps=["Get D.Pharma degree or hire qualified pharmacist", "Apply drug license (State FDA)", "Source from authorized distributor"],
                risks=["Regulatory compliance", "Qualified pharmacist salary", "Expiry management"],
                success_rate="85%",
            ))

        if capital >= 300000 and (p.age <= 45):
            paths.append(CareerPath(
                path_name="Cloud Kitchen / Restaurant",
                description="Dark kitchen model (delivery only). Lower investment than dine-in, high order volume.",
                capital_needed=280000,
                timeline_months=3,
                expected_monthly_income=120000,
                first_steps=["Register on Swiggy SNACC / Zomato for Restaurants", "Get FSSAI license + kitchen NOC", "Develop 15-item focused menu"],
                risks=["Delivery platform commission 25-30%", "Consistent food quality", "Supply chain"],
                success_rate="68%",
            ))

        if p.is_woman and capital >= 20000:
            paths.append(CareerPath(
                path_name="Self-Help Group (SHG) Micro Enterprise",
                description="Form or join a SHG. Access group loans, government contracts, NRLM support.",
                capital_needed=5000,
                timeline_months=3,
                expected_monthly_income=15000,
                first_steps=["Register SHG with 10+ women", "Open SHG bank account", "Apply for NRLM Community Investment Fund"],
                risks=["Group dynamics", "Collective decision-making", "Market linkage"],
                success_rate="78%",
            ))

        paths.sort(key=lambda x: (-x.expected_monthly_income, x.capital_needed))
        return paths[:5]

    def _check_government_eligibility(self, p: IdentityProfile) -> List[GovernmentEligibility]:
        eligibilities = []

        eligibilities.append(GovernmentEligibility(
            scheme_id="mudra_shishu", scheme_name="MUDRA Shishu", ministry="MUDRA / MoF",
            max_benefit="Rs.50,000 no-collateral loan",
            eligible=p.capital < 100000,
            reason="Capital below Rs.1 lakh — eligible for microenterprise loan",
            action_required="Visit any nationalized bank with Aadhaar + PAN",
            priority="immediate",
        ))

        eligibilities.append(GovernmentEligibility(
            scheme_id="pm_svanidhi", scheme_name="PM SVANidhi", ministry="MoHUA",
            max_benefit="Rs.10,000 → Rs.50,000 in stages with cashback",
            eligible=p.capital < 20000,
            reason="Micro capital — perfect for street vending",
            action_required="Apply at pmsvanidhi.mohua.gov.in or nearest CSC",
            priority="immediate" if p.capital < 20000 else "low",
        ))

        eligibilities.append(GovernmentEligibility(
            scheme_id="pmegp", scheme_name="PMEGP", ministry="Ministry of MSME",
            max_benefit="Rs.25 lakh loan with 15-35% govt subsidy",
            eligible=p.capital >= 50000 and EDUCATION_LEVELS.get(p.education,4) >= 4,
            reason="Has basic capital and education threshold (8th pass for projects > Rs.10 lakh)",
            action_required="Apply at kviconline.gov.in — need project report",
            priority="medium",
        ))

        if p.is_woman:
            eligibilities.append(GovernmentEligibility(
                scheme_id="mahila_udyam_nidhi", scheme_name="Mahila Udyam Nidhi", ministry="SIDBI",
                max_benefit="Up to Rs.10 lakh at concessional rate for women",
                eligible=True,
                reason="Woman entrepreneur — special soft loan available",
                action_required="Apply through nearest SIDBI or nationalized bank",
                priority="immediate",
            ))
            eligibilities.append(GovernmentEligibility(
                scheme_id="wdc_loan", scheme_name="Women Dev. Corporation Loan", ministry="State Government",
                max_benefit="Rs.2 lakh at 4-8% interest",
                eligible=True,
                reason="State-level scheme for women — very low interest",
                action_required="Visit State Women & Child Development Department",
                priority="medium",
            ))

        if p.caste_category in ["sc","st"]:
            eligibilities.append(GovernmentEligibility(
                scheme_id="stand_up_india", scheme_name="Stand-Up India", ministry="Ministry of Finance",
                max_benefit="Rs.10 lakh – Rs.1 crore for greenfield enterprise",
                eligible=True,
                reason=f"SC/ST category — exclusive scheme access",
                action_required="Apply at standupmitra.in or any scheduled commercial bank",
                priority="immediate",
            ))

        if p.caste_category == "obc":
            eligibilities.append(GovernmentEligibility(
                scheme_id="obc_nbc", scheme_name="OBC & Minority Welfare Loan", ministry="MoSJE",
                max_benefit="Rs.20 lakh at subsidized rate",
                eligible=True,
                reason="OBC category — National Backward Classes Finance Corporation loan",
                action_required="Apply at nbcfdc.nic.in or State BC/MBC Development Corporation",
                priority="medium",
            ))

        eligibilities.append(GovernmentEligibility(
            scheme_id="udyam", scheme_name="Udyam Registration (MSME)", ministry="Ministry of MSME",
            max_benefit="Free registration — unlocks all MSME benefits, tender eligibility, credit guarantee",
            eligible=True,
            reason="Any micro/small enterprise can register — mandatory to access other schemes",
            action_required="Register free at udyamregistration.gov.in in 5 minutes",
            priority="immediate",
        ))

        if EDUCATION_LEVELS.get(p.education, 4) <= 4:
            eligibilities.append(GovernmentEligibility(
                scheme_id="pmkvy", scheme_name="PMKVY Skill Training", ministry="MoSDE",
                max_benefit="Free skill training + Rs.500-Rs.1500 stipend per month",
                eligible=True,
                reason="Skill training improves income by 40-60%",
                action_required="Find nearest PMKVY training centre at smarth.nsdcindia.org",
                priority="immediate" if EDUCATION_LEVELS.get(p.education,4) <= 4 else "medium",
            ))

        eligibilities.sort(key=lambda x: {"immediate": 0, "medium": 1, "low": 2}[x.priority])
        return eligibilities[:7]

    def _identify_skill_gaps(self, p: IdentityProfile) -> List[SkillGap]:
        gaps = []
        skills = [s.lower() for s in p.skills]

        if "computers" not in skills and "digital" not in skills:
            gaps.append(SkillGap(
                skill_name="Basic Computer & Digital Literacy",
                importance="critical",
                learning_time_days=30,
                free_resource="Google Digital Garage — free online course",
                government_course="PMKVY IT Basics — free at nearest centre",
                expected_income_boost="+15-25% income — digital billing, UPI, online presence",
            ))

        if "english" not in skills and "any" in skills:
            gaps.append(SkillGap(
                skill_name="Basic Business English",
                importance="high",
                learning_time_days=45,
                free_resource="BBC Learning English app + YouTube: Spoken English lessons",
                government_course="PMKVY English Speaking — free",
                expected_income_boost="+20% — client confidence, premium pricing ability",
            ))

        if "accounting" not in skills and "selling" not in skills:
            gaps.append(SkillGap(
                skill_name="Basic Accounting & GST Filing",
                importance="high",
                learning_time_days=21,
                free_resource="YouTube: Tally with GST tutorials",
                government_course="NSDC Accounts Assistant course",
                expected_income_boost="+10-15% — avoid CA fees, ensure compliance",
            ))

        if "selling" not in skills:
            gaps.append(SkillGap(
                skill_name="Sales & Customer Service",
                importance="medium",
                learning_time_days=14,
                free_resource="YouTube: Sales techniques for small business India",
                government_course="NSDC Retail Skills Training",
                expected_income_boost="+20-30% revenue — better closing, repeat customers",
            ))

        if p.capital < 50000 and "any" in skills:
            gaps.append(SkillGap(
                skill_name="One Specific Vocational Skill",
                importance="critical",
                learning_time_days=45,
                free_resource="YouTube: Learn tailoring / mobile repair / cooking",
                government_course="PMKVY — choose from 200+ courses, all free",
                expected_income_boost="Doubles income potential — skill = product, product = income",
            ))

        return gaps[:4]

    def _identify_strengths(self, p: IdentityProfile) -> List[str]:
        strengths = []
        if p.age < 35:
            strengths.append(f"Young entrepreneur ({p.age} years) — energy and adaptability advantage")
        if len(p.skills) >= 3:
            strengths.append(f"Multi-skilled ({', '.join(p.skills[:3])}) — can combine skills for unique offering")
        if p.is_woman:
            strengths.append("Woman entrepreneur — access to exclusive schemes, SHG networks, lower competition")
        if p.has_space:
            strengths.append("Has physical space — saves Rs.5,000-30,000/month rent, immediate launch possible")
        if p.capital >= 50000:
            strengths.append(f"Rs.{p.capital:,.0f} capital — eligible for shop-based businesses, no loan needed for many options")
        if p.caste_category in ["sc","st","obc"]:
            strengths.append(f"{p.caste_category.upper()} category — higher subsidy (35%) in PMEGP, Stand-Up India access")
        if len(p.languages) >= 2:
            strengths.append(f"Multilingual ({', '.join(p.languages[:3])}) — can serve diverse customer base")
        if EDUCATION_LEVELS.get(p.education,4) >= 7:
            strengths.append(f"Higher education ({p.education}) — eligible for larger loans, professional services")
        return strengths[:5]

    def _identify_challenges(self, p: IdentityProfile) -> List[str]:
        challenges = []
        if p.capital < 20000:
            challenges.append("Limited startup capital — focus on zero/low-investment business models first")
        if EDUCATION_LEVELS.get(p.education,4) < 4:
            challenges.append("Low formal education — certain regulated businesses (pharmacy, clinic) need qualification")
        if p.risk_appetite == "low":
            challenges.append("Low risk tolerance — stick to proven business models with predictable cash flow")
        if p.age > 50:
            challenges.append("Late start — focus on businesses with quick returns and family succession plan")
        if not p.has_space:
            challenges.append("No existing space — budget for security deposit (3 months rent) + interior work")
        if len(p.skills) <= 1 and p.skills == ["any"]:
            challenges.append("No identified core skills — skill development is the #1 priority before investment")
        return challenges[:4]

    def _immediate_actions(self, p: IdentityProfile, paths: List[CareerPath]) -> List[str]:
        actions = []
        actions.append("1. Register on Udyam (udyamregistration.gov.in) — free, takes 5 minutes, unlocks all MSME benefits")

        if p.capital < 20000:
            actions.append("2. Apply PM SVANidhi at pmsvanidhi.mohua.gov.in — Rs.10,000 in 5 days, no collateral")
        else:
            actions.append(f"2. Open a Current Account at nearest bank — required for business transactions")

        if len(p.skills) <= 1:
            actions.append("3. Enroll in PMKVY free skill course — 30-90 day program, changes income permanently")
        else:
            top_path = paths[0].path_name if paths else "Tea Stall"
            actions.append(f"3. Visit 5 existing similar businesses in your area — best market research before starting")

        actions.append("4. Get FSSAI Basic Registration (free, online) — needed for any food-related business")

        if p.is_woman:
            actions.append("5. Contact nearest Mahila Udyam Nidhi / Women Dev. Corporation — exclusive soft loans")
        elif p.caste_category in ["sc","st"]:
            actions.append("5. Contact Stand-Up India nodal officer at nearest bank — up to Rs.1 crore SC/ST loan")
        else:
            actions.append("5. Visit nearest MUDRA-registered bank — tell them your business plan, get Shishu loan")

        return actions

    def _income_potential(self, p: IdentityProfile) -> float:
        base = 15000
        base += EDUCATION_LEVELS.get(p.education, 4) * 2000
        base += len(p.skills) * 3000
        if p.capital >= 100000: base += 30000
        elif p.capital >= 50000: base += 15000
        elif p.capital >= 20000: base += 8000
        if p.age < 35: base += 5000
        return round(base)

    def _digital_literacy_score(self, p: IdentityProfile) -> float:
        score = 0.0
        skills = [s.lower() for s in p.skills]
        if "computers" in skills or "digital" in skills: score += 40
        if EDUCATION_LEVELS.get(p.education, 4) >= 6: score += 20
        if p.age < 35: score += 20
        elif p.age < 45: score += 10
        if len(p.languages) >= 2: score += 10
        return min(100, score)

    def _generate_summary(self, p: IdentityProfile, score: float, paths: List[CareerPath]) -> str:
        tier_msg = {
            "street_vendor": f"{p.person_name} has Rs.{p.capital:,.0f} to start with — the best immediate path is a street vending or home-based business.",
            "micro_entrepreneur": f"{p.person_name} is well-positioned for a micro-enterprise with Rs.{p.capital:,.0f}.",
            "small_business": f"{p.person_name} has solid capital of Rs.{p.capital:,.0f} for a proper shop-based business.",
            "sme_owner": f"{p.person_name} can launch a significant business with Rs.{p.capital:,.0f}.",
            "medium_enterprise": f"{p.person_name} has strong capital Rs.{p.capital:,.0f} for a medium-scale enterprise.",
        }
        tier = self._economic_tier(p.capital)
        base = tier_msg.get(tier, f"{p.person_name} has good potential.")

        best_path = paths[0].path_name if paths else "a suitable business"
        return f"{base} Opportunity Score: {score}/100. Top recommended path: {best_path} with {paths[0].expected_monthly_income:,.0f}/month potential. {len(paths)} personalized paths identified."

    def _generate_hindi_summary(self, p: IdentityProfile, score: float) -> str:
        return (f"{p.person_name} के लिए अवसर स्कोर {score}/100 है। "
                f"आपके पास Rs.{p.capital:,.0f} पूंजी है। "
                f"सरकारी योजनाओं के तहत बिना गारंटी के ऋण मिल सकता है। "
                f"आज ही उद्यम रजिस्ट्रेशन करें — यह मुफ्त है।")
