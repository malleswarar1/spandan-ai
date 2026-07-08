"""
SPANDAN AI — Autonomous Business Space Designer

Generates optimized floor plans, equipment placement, cost estimates,
and compliance notes for any business type given dimensions and budget.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import math, logging

logger = logging.getLogger("spandan.space")

@dataclass
class Zone:
    id: str
    name: str
    x: float        # feet from left wall
    y: float        # feet from front wall
    w: float        # width in feet
    h: float        # depth in feet
    color: str      # hex color for rendering
    icon: str       # emoji icon
    pct_of_total: float
    purpose: str
    notes: str = ""

@dataclass
class Equipment:
    id: str
    name: str
    x: float
    y: float
    w: float
    h: float
    icon: str
    quantity: int
    unit_cost: float
    total_cost: float
    priority: str   # essential / recommended / optional
    notes: str = ""

@dataclass
class SpaceDesignResult:
    business_type: str
    display_name: str
    total_area: float
    width_ft: float
    depth_ft: float
    budget: float
    zones: List[Zone]
    equipment: List[Equipment]
    cost_breakdown: Dict
    efficiency_score: float
    compliance_notes: List[str]
    optimization_tips: List[str]
    layout_style: str
    customer_flow: str
    estimated_setup_cost: float
    estimated_monthly_revenue: float
    design_version: str = "v2"


TEMPLATES = {
    "grocery": {
        "display_name": "Grocery / Kirana Store",
        "min_area": 150,
        "ideal_area": 400,
        "layout_style": "linear",
        "customer_flow": "Enter → Browse aisles → Counter → Exit",
        "zones": [
            {"id":"entrance","name":"Entrance / Display","pct":0.08,"color":"#1a3d2e","icon":"🚪","purpose":"Entry and impulse-buy displays"},
            {"id":"main_floor","name":"Shopping Floor","pct":0.40,"color":"#0d2235","icon":"🛒","purpose":"Customer browsing aisles"},
            {"id":"wall_shelves","name":"Wall Display Racks","pct":0.15,"color":"#2d1a0a","icon":"📦","purpose":"Packaged goods, FMCG products"},
            {"id":"counter","name":"Counter / POS Area","pct":0.10,"color":"#2d1a2d","icon":"🧾","purpose":"Billing, cash, digital payments"},
            {"id":"cold_zone","name":"Cooling Zone","pct":0.07,"color":"#0a2040","icon":"❄️","purpose":"Dairy, beverages, fresh produce"},
            {"id":"storage","name":"Storage / Backroom","pct":0.15,"color":"#1a1a2d","icon":"📫","purpose":"Stock, supplies, non-display items"},
            {"id":"utilities","name":"Utilities / WC","pct":0.05,"color":"#1a2a1a","icon":"🚿","purpose":"Staff restroom, utility area"},
        ],
        "equipment": [
            {"id":"counter","name":"Checkout Counter","w":4,"h":2.5,"icon":"🧾","qty":1,"cost":8000,"priority":"essential","notes":"With display shelf below"},
            {"id":"display_rack","name":"Display Rack (4-shelf)","w":3,"h":1.5,"icon":"📦","qty":6,"cost":3500,"priority":"essential","notes":"Place along walls and center"},
            {"id":"refrigerator","name":"Vertical Refrigerator","w":2.5,"h":2,"icon":"🧊","qty":2,"cost":22000,"priority":"essential","notes":"For dairy, cold drinks"},
            {"id":"weighing","name":"Digital Weighing Scale","w":0.8,"h":0.8,"icon":"⚖️","qty":2,"cost":2500,"priority":"essential","notes":"Counter top model"},
            {"id":"scanner","name":"Barcode Scanner + POS","w":0.5,"h":0.3,"icon":"📟","qty":1,"cost":8000,"priority":"recommended","notes":"Reduces billing time 60%"},
            {"id":"cctv","name":"CCTV Camera","w":0.3,"h":0.3,"icon":"📷","qty":4,"cost":3500,"priority":"recommended","notes":"Deter theft, 4-corner coverage"},
            {"id":"signboard","name":"LED Signboard","w":5,"h":1,"icon":"💡","qty":1,"cost":5000,"priority":"recommended","notes":"Visible from main road"},
            {"id":"cash_drawer","name":"Cash Drawer + Tray","w":0.5,"h":0.3,"icon":"💰","qty":1,"cost":1500,"priority":"essential","notes":"Secure cash management"},
            {"id":"ceiling_fan","name":"Ceiling Fan","w":1,"h":1,"icon":"💨","qty":3,"cost":2500,"priority":"essential","notes":"Customer comfort"},
        ],
        "compliance": [
            "FSSAI Basic Registration (free, 5-year validity) — mandatory for food items",
            "Shop and Establishment Act license from local municipal authority",
            "GST registration if turnover > Rs.20 lakh/year",
            "Trade license from Municipal Corporation",
            "Weights & Measures certification for weighing scales",
            "Fire safety compliance — keep exit clear, fire extinguisher at counter",
        ],
        "tips": [
            "Place high-margin impulse items (chocolates, gum, batteries) at the counter",
            "Eye-level shelves (3–5 feet) should have your fastest-moving items",
            "Cold zone near entry boosts daily footfall with dairy/beverage shoppers",
            "QR payment boards increase basket size by 15% — customers spend more digitally",
            "Narrow 3-foot aisles slow customers down, increasing purchase probability",
        ],
    },
    "salon": {
        "display_name": "Beauty Salon / Parlour",
        "min_area": 200,
        "ideal_area": 400,
        "layout_style": "workstation",
        "customer_flow": "Reception → Waiting → Styling → Wash → Dryer → Checkout",
        "zones": [
            {"id":"reception","name":"Reception & Waiting","pct":0.18,"color":"#2d1a3d","icon":"🪑","purpose":"Client check-in, waiting, product display"},
            {"id":"styling","name":"Styling Stations","pct":0.40,"color":"#1a0d2d","icon":"✂️","purpose":"Hair cutting, styling, makeup"},
            {"id":"wash_area","name":"Wash Area","pct":0.18,"color":"#0a1a3d","icon":"🚿","purpose":"Hair washing, conditioning, treatment"},
            {"id":"dryer_zone","name":"Dryer / Treatment Zone","pct":0.10,"color":"#2d2d0a","icon":"💨","purpose":"Blow dry, hair treatment, setting"},
            {"id":"storage","name":"Product Storage","pct":0.08,"color":"#1a1a2d","icon":"📦","purpose":"Chemicals, towels, equipment stock"},
            {"id":"staff_restroom","name":"Staff / Client WC","pct":0.06,"color":"#1a2a1a","icon":"🚿","purpose":"Essential hygiene facility"},
        ],
        "equipment": [
            {"id":"styling_chair","name":"Styling Chair (hydraulic)","w":2,"h":2.5,"icon":"💺","qty":3,"cost":7000,"priority":"essential","notes":"Hydraulic for easy height adjustment"},
            {"id":"mirror","name":"Full-length Mirror with Light","w":2,"h":0.5,"icon":"🪞","qty":3,"cost":5000,"priority":"essential","notes":"LED frame mirrors — client engagement"},
            {"id":"wash_basin","name":"Hair Wash Basin + Chair","w":2.5,"h":3,"icon":"🚿","qty":2,"cost":12000,"priority":"essential","notes":"Reclining chair + ceramic basin"},
            {"id":"dryer","name":"Professional Hair Dryer","w":0.3,"h":0.3,"icon":"💨","qty":3,"cost":3500,"priority":"essential","notes":"1800W+"},
            {"id":"reception_desk","name":"Reception Desk","w":3.5,"h":2,"icon":"🖥️","qty":1,"cost":6000,"priority":"essential","notes":"With product display shelf"},
            {"id":"waiting_sofa","name":"Waiting Sofa","w":4,"h":1.5,"icon":"🪑","qty":1,"cost":8000,"priority":"essential","notes":"Comfortable, durable"},
            {"id":"product_shelf","name":"Product Display Shelf","w":1,"h":3,"icon":"🧴","qty":2,"cost":2500,"priority":"recommended","notes":"Sell retail products — 20% extra revenue"},
            {"id":"sterilizer","name":"UV Sterilizer Box","w":0.8,"h":0.5,"icon":"🧹","qty":1,"cost":1500,"priority":"essential","notes":"Mandatory hygiene — sterilize scissors, combs"},
            {"id":"ac","name":"Split AC (1.5 ton)","w":1,"h":0.5,"icon":"❄️","qty":1,"cost":38000,"priority":"recommended","notes":"Increases client retention significantly"},
        ],
        "compliance": [
            "Municipal Corporation trade license / shop establishment certificate",
            "No specific beauty salon licensing required — GST if revenue > Rs.20 lakh",
            "NSDC-certified beautician certificate preferred for credibility",
            "Hygiene compliance: sterilized tools, clean towels for each client",
            "Ventilation required for chemical odors (bleach, perm solutions)",
            "Clear price menu displayed at reception — consumer protection requirement",
        ],
        "tips": [
            "Place retail product display near reception — impulse purchases add 15-25% revenue",
            "Styling stations against mirrors on one wall + wash basins on opposite wall = maximum efficiency",
            "Waiting zone near entrance showcases your work (display posters, before/after)",
            "Book appointments on WhatsApp — reduces idle chair time by 30%",
            "Offer Rs.99 express service during off-peak hours to fill capacity",
        ],
    },
    "restaurant": {
        "display_name": "Restaurant / Dhaba / Eatery",
        "min_area": 400,
        "ideal_area": 800,
        "layout_style": "service_flow",
        "customer_flow": "Entrance → Host/Cashier → Dining → Kitchen Delivery → Exit",
        "zones": [
            {"id":"entrance","name":"Entrance & Waiting","pct":0.06,"color":"#1a2d1a","icon":"🚪","purpose":"Host station, waiting queue, menu display"},
            {"id":"dining","name":"Main Dining Area","pct":0.48,"color":"#0d1a2d","icon":"🍽️","purpose":"Customer seating — tables and chairs"},
            {"id":"service_corridor","name":"Service Corridor","pct":0.06,"color":"#2d2d0a","icon":"👨‍🍳","purpose":"Waiter movement path, hot delivery"},
            {"id":"kitchen","name":"Kitchen","pct":0.28,"color":"#2d0a0a","icon":"🔥","purpose":"Food preparation, cooking stations"},
            {"id":"pantry","name":"Pantry / Storage","pct":0.07,"color":"#1a1a2d","icon":"📦","purpose":"Dry goods, cold storage, cleaning"},
            {"id":"restrooms","name":"Restrooms","pct":0.05,"color":"#1a2a1a","icon":"🚿","purpose":"Guest toilets — mandatory above 50 covers"},
        ],
        "equipment": [
            {"id":"dining_table","name":"4-seater Dining Table","w":3,"h":3,"icon":"🪑","qty":8,"cost":4500,"priority":"essential","notes":"Sturdy, easy clean laminate top"},
            {"id":"dining_chair","name":"Dining Chair","w":1.5,"h":1.5,"icon":"🪑","qty":32,"cost":900,"priority":"essential","notes":"Stackable preferred for flexibility"},
            {"id":"burner","name":"Commercial Gas Burner (4-ring)","w":2.5,"h":2,"icon":"🔥","qty":2,"cost":12000,"priority":"essential","notes":"Heavy-duty for high volume"},
            {"id":"refrigerator","name":"Commercial Refrigerator","w":3,"h":2,"icon":"🧊","qty":1,"cost":35000,"priority":"essential","notes":"200L+ capacity"},
            {"id":"exhaust","name":"Exhaust Hood + Fan","w":3,"h":0.5,"icon":"💨","qty":1,"cost":8000,"priority":"essential","notes":"Kitchen ventilation — mandatory safety"},
            {"id":"tandoor","name":"Tandoor Oven","w":1.5,"h":1.5,"icon":"🫓","qty":1,"cost":15000,"priority":"optional","notes":"If serving tandoori items"},
            {"id":"pos","name":"POS Terminal + Printer","w":0.5,"h":0.5,"icon":"📟","qty":1,"cost":12000,"priority":"recommended","notes":"KOT printing saves kitchen errors"},
            {"id":"water_filter","name":"Water Purifier (RO)","w":0.5,"h":0.5,"icon":"💧","qty":1,"cost":8000,"priority":"essential","notes":"FSSAI compliance + quality"},
            {"id":"hand_wash","name":"Hand Wash Station","w":1,"h":0.8,"icon":"🤲","qty":2,"cost":3000,"priority":"essential","notes":"Kitchen + dining area — hygiene"},
        ],
        "compliance": [
            "FSSAI State/Central License — mandatory, apply at foscos.fssai.gov.in",
            "Fire NOC from local fire department",
            "Building plan approval with kitchen ventilation",
            "Eating House License from local police (most states)",
            "GST registration — mandatory for restaurants",
            "Signboard permission from municipality",
            "Pest control certification — do quarterly",
            "Staff health certificates — all kitchen staff",
        ],
        "tips": [
            "Kitchen to dining ratio 30:70 is industry optimal — maximize revenue-generating space",
            "1.5-foot service corridor between kitchen and dining prevents collision accidents",
            "Tables of 4 can be pushed together for 8 — flexible seating doubles capacity",
            "Place cashier/POS near exit — impulse dessert/cold drink purchases before leaving",
            "Lunch-only menu 11am-3pm with delivery reduces waste and maximizes kitchen ROI",
        ],
    },
    "cafe": {
        "display_name": "Cafe / Coffee Shop",
        "min_area": 250,
        "ideal_area": 600,
        "layout_style": "open_plan",
        "customer_flow": "Entrance → Order Counter → Wait → Seating → WiFi Zone",
        "zones": [
            {"id":"entrance","name":"Entrance & Display","pct":0.05,"color":"#1a2d2d","icon":"☕","purpose":"Menu boards, signage, first impression"},
            {"id":"counter","name":"Order & Coffee Counter","pct":0.15,"color":"#2d1a0a","icon":"☕","purpose":"Barista station, POS, display pastries"},
            {"id":"seating_main","name":"Main Seating Area","pct":0.45,"color":"#0d1a2d","icon":"🪑","purpose":"Regular tables, chairs"},
            {"id":"cozy_zone","name":"Cozy / Lounge Zone","pct":0.15,"color":"#2d1a2d","icon":"🛋️","purpose":"Sofas, low tables, laptop users"},
            {"id":"prep_kitchen","name":"Prep Kitchen","pct":0.14,"color":"#2d0a0a","icon":"🔧","purpose":"Coffee machines, sandwich prep, storage"},
            {"id":"restroom","name":"Restrooms","pct":0.06,"color":"#1a2a1a","icon":"🚿","purpose":"Essential — clean restroom = retention"},
        ],
        "equipment": [
            {"id":"espresso","name":"Semi-auto Espresso Machine","w":1.5,"h":0.8,"icon":"☕","qty":1,"cost":55000,"priority":"essential","notes":"Expobar or La Cimbali recommended"},
            {"id":"grinder","name":"Commercial Coffee Grinder","w":0.5,"h":0.4,"icon":"⚙️","qty":1,"cost":15000,"priority":"essential","notes":"Grind fresh per order"},
            {"id":"pos","name":"POS Terminal","w":0.5,"h":0.4,"icon":"📟","qty":1,"cost":10000,"priority":"essential","notes":"With UPI/card integration"},
            {"id":"display_fridge","name":"Glass Display Fridge (cakes/pastries)","w":2,"h":1,"icon":"🎂","qty":1,"cost":25000,"priority":"essential","notes":"Impulse buy driver"},
            {"id":"table_2","name":"2-seater Table","w":2.5,"h":2.5,"icon":"🪑","qty":6,"cost":3500,"priority":"essential","notes":"Compact, easy to rearrange"},
            {"id":"table_4","name":"4-seater Table","w":3.5,"h":3,"icon":"🪑","qty":3,"cost":5000,"priority":"essential","notes":"For group customers"},
            {"id":"sofa","name":"2-seater Sofa","w":4,"h":2,"icon":"🛋️","qty":2,"cost":12000,"priority":"recommended","notes":"For lounge zone"},
            {"id":"wifi_router","name":"High-speed WiFi Router","w":0.2,"h":0.2,"icon":"📶","qty":2,"cost":4000,"priority":"essential","notes":"WiFi is top reason customers return"},
            {"id":"blender","name":"Commercial Blender","w":0.4,"h":0.4,"icon":"🥤","qty":2,"cost":5000,"priority":"essential","notes":"For cold coffee, shakes"},
        ],
        "compliance": [
            "FSSAI License (State level for cafes)",
            "Shop and Establishment Act certificate",
            "GST registration mandatory",
            "Fire extinguisher and NOC",
            "Music license (if playing music) — PPL + IPRS",
            "Eating house license (state-dependent)",
        ],
        "tips": [
            "WiFi password visible at the counter — drives visit frequency",
            "Lounge zone near windows — laptop workers stay 2-4 hours, high per-table revenue",
            "Menu board with upsell suggestions (cold + hot combo, add snack) increases average spend 25%",
            "Counter at front, seating deep inside — customers pass all display items walking to seats",
            "Weekend brunches (10am-2pm) with brunch menu can triple Saturday revenue",
        ],
    },
    "pharmacy": {
        "display_name": "Medical Store / Pharmacy",
        "min_area": 200,
        "ideal_area": 350,
        "layout_style": "prescription_flow",
        "customer_flow": "Enter → Counter → Prescription review → Medicine pickup → OTC browse → Pay",
        "zones": [
            {"id":"counter","name":"Main Counter","pct":0.20,"color":"#0a2d1a","icon":"💊","purpose":"Pharmacist station, prescription verification"},
            {"id":"prescription_area","name":"Prescription Storage","pct":0.15,"color":"#1a0d2d","icon":"📋","purpose":"Filed prescriptions, controlled substances"},
            {"id":"otc_display","name":"OTC Display Area","pct":0.30,"color":"#0d1a3d","icon":"🏥","purpose":"Non-prescription medicines, vitamins, wellness"},
            {"id":"cold_storage","name":"Cold Storage Medicines","pct":0.08,"color":"#0a1a3d","icon":"❄️","purpose":"Insulin, vaccines, refrigerated meds"},
            {"id":"bulk_storage","name":"Bulk Storage","pct":0.20,"color":"#1a1a2d","icon":"📦","purpose":"Stock medicines, supplies"},
            {"id":"utilities","name":"Utilities & WC","pct":0.07,"color":"#1a2a1a","icon":"🚿","purpose":"Staff area, utility"},
        ],
        "equipment": [
            {"id":"dispensing_counter","name":"Dispensing Counter (L-shape)","w":5,"h":3,"icon":"💊","qty":1,"cost":25000,"priority":"essential","notes":"L-shape for prescription and billing"},
            {"id":"medicine_racks","name":"Medicine Storage Rack (labeled)","w":3,"h":2,"icon":"🗃️","qty":6,"cost":4500,"priority":"essential","notes":"Alphabetical or therapeutic classification"},
            {"id":"refrigerator","name":"Medical Grade Refrigerator","w":2,"h":2,"icon":"❄️","qty":1,"cost":28000,"priority":"essential","notes":"2–8°C for insulin, vaccines"},
            {"id":"pos","name":"Pharmacy POS + Billing","w":0.5,"h":0.5,"icon":"📟","qty":1,"cost":15000,"priority":"essential","notes":"GST billing, stock management"},
            {"id":"ac","name":"Split AC (1 ton)","w":1,"h":0.5,"icon":"❄️","qty":1,"cost":30000,"priority":"essential","notes":"Medicine storage temperature control"},
            {"id":"otc_display_shelf","name":"OTC Product Display Stand","w":1.5,"h":3,"icon":"🏪","qty":3,"cost":3500,"priority":"recommended","notes":"Vitamins, health supplements, cosmetics"},
            {"id":"cctv","name":"CCTV System","w":0.3,"h":0.3,"icon":"📷","qty":3,"cost":4000,"priority":"essential","notes":"Compliance + anti-theft"},
        ],
        "compliance": [
            "Drug License — Form 20 & 21 from State Drug Control Authority (mandatory)",
            "D.Pharm or B.Pharm certificate — must be displayed",
            "GST registration mandatory",
            "Shop & Establishment license",
            "Narcotic Drug Register — if stocking Schedule H/H1 drugs",
            "Refrigerator temperature log — daily record mandatory for cold chain",
            "No prescription required for OTC, but Schedule H drugs need valid prescription",
        ],
        "tips": [
            "Display health supplements and OTC products at eye level — 30% extra revenue",
            "Build relationship with nearby doctors — prescription referrals = guaranteed daily revenue",
            "Home delivery in 1km radius via WhatsApp — reorders 3x more likely",
            "Stock Jan Aushadhi medicines — attracts price-sensitive customers + goodwill",
            "Night duty (10pm–6am) if near hospital — competitor-free, high markup margins",
        ],
    },
    "gym": {
        "display_name": "Fitness Centre / Gym",
        "min_area": 800,
        "ideal_area": 2000,
        "layout_style": "zone_based",
        "customer_flow": "Entry → Locker → Cardio Zone → Weight Zone → Stretching → Locker → Exit",
        "zones": [
            {"id":"reception","name":"Reception & Entry","pct":0.07,"color":"#2d1a1a","icon":"💪","purpose":"Membership desk, POS, supplement display"},
            {"id":"locker","name":"Locker Room & WC","pct":0.10,"color":"#1a2a1a","icon":"🔑","purpose":"Separate men/women lockers, showers"},
            {"id":"cardio","name":"Cardio Zone","pct":0.28,"color":"#0d1a2d","icon":"🏃","purpose":"Treadmills, cycles, ellipticals"},
            {"id":"weights","name":"Free Weights Zone","pct":0.30,"color":"#2d0a0a","icon":"🏋️","purpose":"Dumbbells, barbells, benches, squat rack"},
            {"id":"machines","name":"Machine Zone","pct":0.18,"color":"#0a2d1a","icon":"⚙️","purpose":"Cable machines, chest press, leg press"},
            {"id":"functional","name":"Functional / Group Training","pct":0.07,"color":"#2d2d0a","icon":"🧘","purpose":"Group fitness, yoga, HIIT classes"},
        ],
        "equipment": [
            {"id":"treadmill","name":"Commercial Treadmill","w":2.5,"h":1,"icon":"🏃","qty":4,"cost":55000,"priority":"essential","notes":"3-4HP motor minimum for commercial use"},
            {"id":"cycle","name":"Upright Exercise Cycle","w":1,"h":1.5,"icon":"🚴","qty":3,"cost":18000,"priority":"essential","notes":"Magnetic resistance, digital display"},
            {"id":"dumbbell_set","name":"Dumbbell Set (5-50kg)","w":3,"h":0.5,"icon":"💪","qty":1,"cost":45000,"priority":"essential","notes":"Hex rubber dumbbells, full set"},
            {"id":"barbell","name":"Olympic Barbell + Plates","w":0.5,"h":0.5,"icon":"🏋️","qty":3,"cost":22000,"priority":"essential","notes":"With 2.5/5/10/20kg plates"},
            {"id":"squat_rack","name":"Power Rack / Squat Rack","w":4,"h":4,"icon":"🏗️","qty":2,"cost":35000,"priority":"essential","notes":"Critical for serious training"},
            {"id":"bench","name":"Adjustable Weight Bench","w":3.5,"h":1,"icon":"🪑","qty":4,"cost":8000,"priority":"essential","notes":"Flat + incline + decline"},
            {"id":"cable_machine","name":"Dual Cable Machine","w":2.5,"h":2,"icon":"⚙️","qty":1,"cost":85000,"priority":"recommended","notes":"Most-used machine in any gym"},
            {"id":"mirror","name":"Wall-to-wall Mirror","w":8,"h":0,"icon":"🪞","qty":2,"cost":12000,"priority":"essential","notes":"Full wall coverage in weight zone"},
            {"id":"ac","name":"Split AC (2 ton)","w":1,"h":0.5,"icon":"❄️","qty":3,"cost":45000,"priority":"essential","notes":"Multiple units for full coverage"},
        ],
        "compliance": [
            "Municipal corporation trade license",
            "Building occupancy certificate — structural safety for heavy equipment",
            "Fire NOC — mandatory for premises above certain size",
            "Certified trainer on premises — CPR certification",
            "First aid kit and AED (defibrillator) — recommended",
            "Member registration with emergency contact",
            "Adequate ventilation — 15 air changes per hour minimum",
        ],
        "tips": [
            "Cardio equipment near windows — natural light boosts workout motivation",
            "Mirror placement in weight zone dramatically increases member satisfaction",
            "Group class area floored with rubber — noise reduction + versatility",
            "Reception supplement display — protein powder sales can be 15% of revenue",
            "Early morning 5-8am + evening 5-9pm = 70% of visits — staff accordingly",
        ],
    },
    "coaching": {
        "display_name": "Coaching Centre / Tuition Class",
        "min_area": 200,
        "ideal_area": 500,
        "layout_style": "classroom",
        "customer_flow": "Entry → Office → Classroom → Library Zone → Exit",
        "zones": [
            {"id":"office","name":"Admin Office & Reception","pct":0.15,"color":"#1a0d2d","icon":"📋","purpose":"Enrollment, fees, parent interaction"},
            {"id":"classroom_1","name":"Main Classroom","pct":0.38,"color":"#0d1a2d","icon":"📚","purpose":"Primary teaching space, 20-30 students"},
            {"id":"classroom_2","name":"Secondary Classroom","pct":0.25,"color":"#0d2d1a","icon":"📐","purpose":"Additional batch, different subject"},
            {"id":"library","name":"Study / Library Zone","pct":0.14,"color":"#2d2d0a","icon":"📖","purpose":"Self-study, reference books, materials"},
            {"id":"utilities","name":"Utilities & WC","pct":0.08,"color":"#1a2a1a","icon":"🚿","purpose":"Staff + student restrooms"},
        ],
        "equipment": [
            {"id":"whiteboard","name":"Large Magnetic Whiteboard","w":6,"h":0.3,"icon":"📋","qty":2,"cost":3500,"priority":"essential","notes":"4×6 feet, wall-mounted"},
            {"id":"student_desk","name":"Student Desk + Chair","w":2,"h":2,"icon":"🪑","qty":25,"cost":1800,"priority":"essential","notes":"Ergonomic for long study sessions"},
            {"id":"teacher_desk","name":"Teacher Desk & Chair","w":3,"h":2,"icon":"🪑","qty":2,"cost":5000,"priority":"essential","notes":"Elevated position for visibility"},
            {"id":"projector","name":"Projector + Screen","w":1,"h":1,"icon":"📽️","qty":1,"cost":18000,"priority":"recommended","notes":"Digital teaching + recorded lectures"},
            {"id":"bookshelf","name":"Bookshelf (reference library)","w":1,"h":3,"icon":"📚","qty":4,"cost":2500,"priority":"recommended","notes":"Study materials, textbooks"},
            {"id":"fan","name":"Ceiling Fan","w":1,"h":1,"icon":"💨","qty":4,"cost":2500,"priority":"essential","notes":"Comfort for long study hours"},
            {"id":"ac","name":"Split AC (1.5 ton)","w":1,"h":0.5,"icon":"❄️","qty":2,"cost":38000,"priority":"recommended","notes":"Summer retention — students leave if hot"},
            {"id":"cctv","name":"CCTV (for safety)","w":0.3,"h":0.3,"icon":"📷","qty":3,"cost":4000,"priority":"recommended","notes":"Parent confidence, safety compliance"},
        ],
        "compliance": [
            "No specific central regulation for private coaching — state rules vary",
            "Shop and Establishment Act license",
            "Fire safety compliance — two exits, fire extinguisher",
            "Adequate lighting — minimum 300 lux for study areas",
            "Building completion certificate",
            "If boarding students — additional residential regulations apply",
        ],
        "tips": [
            "Batch of 20-25 is sweet spot — personal attention + revenue optimization",
            "Whiteboard at the far wall, teacher desk central — all students see clearly",
            "Library/study zone keeps students on premises longer — reduces parental anxiety",
            "Online classes via Google Meet + physical = 40% more students without extra space",
            "Display toppers' photos and results prominently — best marketing for new admissions",
        ],
    },
    "mobile_repair": {
        "display_name": "Mobile Repair Shop",
        "min_area": 80,
        "ideal_area": 150,
        "layout_style": "workbench",
        "customer_flow": "Entry → Diagnosis Counter → Repair Workbench → QC → Pickup",
        "zones": [
            {"id":"counter","name":"Customer Counter","pct":0.20,"color":"#1a2d2d","icon":"📱","purpose":"Customer intake, diagnosis, quote, payment"},
            {"id":"display","name":"Accessory Display","pct":0.25,"color":"#2d1a0a","icon":"🎧","purpose":"Cases, chargers, earphones, accessories"},
            {"id":"workbench","name":"Repair Workbench","pct":0.35,"color":"#0a1a2d","icon":"🔧","purpose":"Technical repair, soldering, parts replacement"},
            {"id":"parts_storage","name":"Parts Storage","pct":0.15,"color":"#1a1a2d","icon":"⚙️","purpose":"Spare parts, screens, batteries organized"},
            {"id":"utilities","name":"Utilities","pct":0.05,"color":"#1a2a1a","icon":"🔌","purpose":"Power, tools, charging rack"},
        ],
        "equipment": [
            {"id":"workbench","name":"Anti-static Work Table","w":4,"h":2,"icon":"🔧","qty":2,"cost":4500,"priority":"essential","notes":"ESD-safe surface, built-in power strip"},
            {"id":"soldering","name":"Soldering Station","w":0.5,"h":0.5,"icon":"🔩","qty":2,"cost":3500,"priority":"essential","notes":"Temperature-controlled for precision"},
            {"id":"microscope","name":"Trinocular Microscope","w":1,"h":1,"icon":"🔬","qty":1,"cost":12000,"priority":"essential","notes":"Board-level repair — huge revenue opportunity"},
            {"id":"screen_opener","name":"Screen Separator (heating plate)","w":0.5,"h":0.5,"icon":"🌡️","qty":1,"cost":3000,"priority":"essential","notes":"For cracked screen replacements"},
            {"id":"parts_cabinet","name":"Parts Storage Cabinet (labeled)","w":2,"h":3,"icon":"🗃️","qty":2,"cost":3000,"priority":"essential","notes":"Organized by brand/model"},
            {"id":"charging_rack","name":"Multi-device Charging Rack","w":1,"h":1,"icon":"🔋","qty":1,"cost":2000,"priority":"recommended","notes":"Hold 10+ devices during repair/QC"},
            {"id":"display_case","name":"Glass Display Case (accessories)","w":3,"h":1,"icon":"🎁","qty":1,"cost":8000,"priority":"essential","notes":"Lock + display for high-value accessories"},
            {"id":"pos","name":"POS + Receipt Printer","w":0.5,"h":0.5,"icon":"📟","qty":1,"cost":8000,"priority":"recommended","notes":"Job card system, payment tracking"},
        ],
        "compliance": [
            "Shop and Establishment Act license",
            "GST registration (if turnover > Rs.20 lakh)",
            "Trade license from municipality",
            "E-waste disposal compliance — dead phones/batteries must go to authorized recyclers",
        ],
        "tips": [
            "Accessories on display drive 30-40% of revenue with zero skill needed",
            "Same-day repair commitment doubles customer trust and repeat visits",
            "WhatsApp status updates during repair — customers love live updates",
            "Empannel with Flipkart/Amazon as authorized service centre for steady work",
            "Screen replacement margins 300-400% — prioritize this skill first",
        ],
    },
    "tea_stall": {
        "display_name": "Tea Stall / Chai Tapri",
        "min_area": 40,
        "ideal_area": 80,
        "layout_style": "counter_only",
        "customer_flow": "Customer approaches counter → Order → Pickup → Stand/Sit nearby",
        "zones": [
            {"id":"cooking","name":"Cooking Station","pct":0.35,"color":"#2d0a0a","icon":"🔥","purpose":"Stove, vessels, milk, sugar storage"},
            {"id":"counter","name":"Customer Counter","pct":0.30,"color":"#2d1a0a","icon":"☕","purpose":"Serving, payment, snack display"},
            {"id":"seating","name":"Seating / Standing Area","pct":0.25,"color":"#0d1a2d","icon":"🪑","purpose":"Benches, stools for customers"},
            {"id":"storage","name":"Storage & Utilities","pct":0.10,"color":"#1a1a2d","icon":"📦","purpose":"Stock, gas cylinder, cleaning"},
        ],
        "equipment": [
            {"id":"stove","name":"Commercial Gas Stove (2-burner)","w":1.5,"h":1,"icon":"🔥","qty":1,"cost":3500,"priority":"essential","notes":"Brass jet, heavy duty"},
            {"id":"vessels","name":"Large Vessels (chai + milk)","w":0.5,"h":0.5,"icon":"🫖","qty":3,"cost":1500,"priority":"essential","notes":"5L, 10L, 20L capacity"},
            {"id":"counter_top","name":"Counter Table (with display)","w":4,"h":1.5,"icon":"🪑","qty":1,"cost":3000,"priority":"essential","notes":"Glass top for snack display"},
            {"id":"bench","name":"Customer Bench","w":4,"h":1,"icon":"🪑","qty":2,"cost":1500,"priority":"recommended","notes":"Simple wooden/iron bench"},
            {"id":"gas_connection","name":"Commercial Gas Cylinder + Regulator","w":0.5,"h":1,"icon":"⚗️","qty":2,"cost":2000,"priority":"essential","notes":"Always keep 1 spare"},
            {"id":"fridge_small","name":"Small Refrigerator (cold drinks)","w":1.5,"h":1,"icon":"🧊","qty":1,"cost":12000,"priority":"recommended","notes":"Cold drinks increase revenue by 40%"},
            {"id":"display_box","name":"Snack Display Box","w":1,"h":0.8,"icon":"🥪","qty":1,"cost":1500,"priority":"recommended","notes":"Samosa, biscuits — impulse purchase"},
        ],
        "compliance": [
            "FSSAI Basic Registration (online, free)",
            "Street Vendor Certificate from local urban body (PM SVANidhi eligibility)",
            "No open fire violations — LPG safety certificate",
            "Food hygiene: boiled water, clean utensils — municipal inspection",
        ],
        "tips": [
            "Location at bus stop, office gate, or market entry = 80% of success",
            "6-9 AM and 4-7 PM = peak hours — be fully stocked at these times",
            "Masala chai differentiation: cardamom, ginger variants — charge Rs.2 premium",
            "Add 'Cutting Chai' (half cup) at Rs.5 — doubles transactions from same customer",
            "Accept Google Pay QR — working people prefer cashless for quick purchases",
        ],
    },
    "vegetable_vendor": {
        "display_name": "Vegetable Cart / Vendor",
        "min_area": 20,
        "ideal_area": 60,
        "layout_style": "cart",
        "customer_flow": "Customer approaches → Browse → Select → Weigh → Pay",
        "zones": [
            {"id":"front_display","name":"Front Display","pct":0.50,"color":"#0d2d0a","icon":"🥬","purpose":"Leafy vegetables, daily specials, eye-catching display"},
            {"id":"weighing","name":"Weighing & Serving Area","pct":0.25,"color":"#1a2d0a","icon":"⚖️","purpose":"Weighing, bagging, payment"},
            {"id":"stock","name":"Stock Storage","pct":0.25,"color":"#1a1a2d","icon":"📦","purpose":"Backup stock, water for freshness"},
        ],
        "equipment": [
            {"id":"cart","name":"Push Cart or Thela (wooden/metal)","w":4,"h":2,"icon":"🛒","qty":1,"cost":4500,"priority":"essential","notes":"Wooden with display ledge or metal frame"},
            {"id":"weighing_scale","name":"Digital Weighing Scale","w":0.5,"h":0.5,"icon":"⚖️","qty":1,"cost":2000,"priority":"essential","notes":"15kg capacity, battery-operated"},
            {"id":"tarpaulin","name":"Tarpaulin / Shade Cover","w":4,"h":3,"icon":"⛱️","qty":1,"cost":800,"priority":"essential","notes":"Rain + sun protection for produce"},
            {"id":"water_container","name":"Water Drum / Sprayer","w":0.5,"h":1,"icon":"💧","qty":1,"cost":500,"priority":"recommended","notes":"Sprinkle water to keep veggies fresh"},
            {"id":"display_basket","name":"Wicker Display Baskets","w":0.5,"h":0.3,"icon":"🧺","qty":8,"cost":150,"priority":"recommended","notes":"Attractive display, categorize by type"},
        ],
        "compliance": [
            "Street Vending Certificate from local urban local body (ULB)",
            "FSSAI Basic Registration (free, annual)",
            "No construction on public right-of-way without vending certificate",
            "PM SVANidhi eligible — use for financing improvements",
        ],
        "tips": [
            "6 AM APMC purchase + 7 AM roadside setup = freshest produce in neighborhood",
            "Residential street with apartments > 200 families = steady customer base",
            "Display large, colorful items (pumpkins, cabbage) at front — attracts attention",
            "Bundle selling: '500g tomato + 250g onion = Rs.25' increases average sale",
            "Pre-cut vegetables in evenings serve working women — charge 20% premium",
        ],
    },
    "clinic": {
        "display_name": "Medical Clinic / Doctor's Clinic",
        "min_area": 300,
        "ideal_area": 600,
        "layout_style": "medical",
        "customer_flow": "Reception → Waiting → Consultation Room → Procedure/Dressing → Pharmacy",
        "zones": [
            {"id":"reception","name":"Reception & Registration","pct":0.15,"color":"#0a2d1a","icon":"📋","purpose":"Patient registration, fees, appointment"},
            {"id":"waiting","name":"Waiting Area","pct":0.20,"color":"#0d1a2d","icon":"🪑","purpose":"Patient waiting — comfortable, hygienic"},
            {"id":"consultation_1","name":"Doctor's Consultation Room 1","pct":0.22,"color":"#1a0d2d","icon":"🩺","purpose":"Primary consultation, examination"},
            {"id":"consultation_2","name":"Consultation Room 2","pct":0.18,"color":"#0d2d1a","icon":"🩺","purpose":"Second doctor or procedures room"},
            {"id":"procedure","name":"Minor Procedure / Dressing Room","pct":0.12,"color":"#2d1a0a","icon":"🩹","purpose":"Dressing changes, injections, minor procedures"},
            {"id":"pharmacy","name":"In-house Pharmacy","pct":0.08,"color":"#1a1a2d","icon":"💊","purpose":"Essential medicines dispensing (optional)"},
            {"id":"restrooms","name":"Patient Restrooms","pct":0.05,"color":"#1a2a1a","icon":"🚿","purpose":"Clean restrooms — patient dignity"},
        ],
        "equipment": [
            {"id":"examination_table","name":"Medical Examination Table","w":2,"h":5,"icon":"🛏️","qty":2,"cost":18000,"priority":"essential","notes":"Adjustable height, easy-clean vinyl"},
            {"id":"doctor_desk","name":"Doctor Desk + Chair","w":3,"h":2,"icon":"🪑","qty":2,"cost":8000,"priority":"essential","notes":"Doctor + attendant + patient chairs"},
            {"id":"bp_monitor","name":"Digital BP Monitor","w":0.3,"h":0.3,"icon":"💉","qty":2,"cost":3500,"priority":"essential","notes":"Keep at reception for initial vitals"},
            {"id":"pulse_oximeter","name":"Pulse Oximeter + Thermometer","w":0.2,"h":0.2,"icon":"🌡️","qty":3,"cost":1500,"priority":"essential","notes":"Basic vitals equipment"},
            {"id":"autoclave","name":"Autoclave Sterilizer","w":1,"h":0.8,"icon":"⚗️","qty":1,"cost":22000,"priority":"essential","notes":"Sterilize instruments — compliance"},
            {"id":"otoscope","name":"Otoscope / Ophthalmoscope","w":0.2,"h":0.2,"icon":"👁️","qty":2,"cost":5000,"priority":"essential","notes":"ENT + eye basics"},
            {"id":"ecg","name":"12-lead ECG Machine","w":0.5,"h":0.5,"icon":"📊","qty":1,"cost":45000,"priority":"recommended","notes":"High-value diagnostic — referral reducer"},
            {"id":"waiting_chairs","name":"Waiting Area Chairs","w":2,"h":1,"icon":"🪑","qty":12,"cost":1200,"priority":"essential","notes":"Comfortable, easy-clean"},
            {"id":"ac","name":"Split AC (1.5 ton) per room","w":1,"h":0.5,"icon":"❄️","qty":3,"cost":38000,"priority":"essential","notes":"Patient comfort, medication storage"},
        ],
        "compliance": [
            "Medical Council registration (MBBS/AYUSH qualification mandatory)",
            "Clinical Establishment Act registration — state-specific",
            "Biomedical Waste Management compliance — separate bins mandatory",
            "Drug License for in-house pharmacy dispensing",
            "NABH certification (optional but increases credibility)",
            "Fire safety compliance",
            "Ramp access for differently-abled — newer regulations",
        ],
        "tips": [
            "Appointment system via WhatsApp/simple app — reduces waiting, increases satisfaction",
            "In-house basic lab tests (blood sugar, urine) — patients prefer one-stop",
            "Health packages (annual check-up Rs.500) drives regular visits",
            "Evening hours 5-9pm captures working population — maximize revenue",
            "Empanel with Ayushman Bharat / PMJAY — steady cashless patient flow",
        ],
    },
    "bakery": {
        "display_name": "Bakery / Sweet Shop",
        "min_area": 200,
        "ideal_area": 400,
        "layout_style": "display_forward",
        "customer_flow": "Entrance → Display Counter → Order → Pickup / Sit",
        "zones": [
            {"id":"display","name":"Display & Sales Counter","pct":0.25,"color":"#2d1a0a","icon":"🍰","purpose":"Glass display of baked goods, cakes, sweets"},
            {"id":"seating","name":"Seating Area (optional)","pct":0.20,"color":"#0d1a2d","icon":"🪑","purpose":"Eat-in customers — increases revenue per visit"},
            {"id":"production","name":"Production Kitchen","pct":0.38,"color":"#2d0a0a","icon":"🔥","purpose":"Oven, mixing, dough preparation"},
            {"id":"cold_storage","name":"Cold Storage & Finishing","pct":0.10,"color":"#0a1a3d","icon":"❄️","purpose":"Cake finishing, decoration, cold items"},
            {"id":"storage","name":"Dry Storage","pct":0.07,"color":"#1a1a2d","icon":"📦","purpose":"Flour, sugar, ingredients, packaging"},
        ],
        "equipment": [
            {"id":"oven","name":"Commercial Convection Oven","w":2,"h":2,"icon":"🔥","qty":1,"cost":45000,"priority":"essential","notes":"4-tray, electric or gas"},
            {"id":"mixer","name":"Planetary Mixer (20L)","w":1.5,"h":1.5,"icon":"⚙️","qty":1,"cost":28000,"priority":"essential","notes":"For dough, batter, cream"},
            {"id":"display_fridge","name":"Glass Display Refrigerator","w":3,"h":1,"icon":"🎂","qty":1,"cost":35000,"priority":"essential","notes":"Front-opening, LED lit — sells product"},
            {"id":"worktop","name":"Stainless Steel Work Table","w":4,"h":2,"icon":"🔧","qty":2,"cost":8000,"priority":"essential","notes":"Hygienic baking surface"},
            {"id":"pos","name":"Billing Counter + POS","w":2,"h":1.5,"icon":"📟","qty":1,"cost":10000,"priority":"essential","notes":"With packaging shelf below"},
            {"id":"cake_fridge","name":"Cake Display Fridge (upright)","w":1.5,"h":1,"icon":"🎂","qty":1,"cost":22000,"priority":"essential","notes":"Customized cakes on display"},
            {"id":"seating_table","name":"2-seater Table","w":2.5,"h":2.5,"icon":"🪑","qty":3,"cost":3000,"priority":"recommended","notes":"Eat-in option"},
        ],
        "compliance": [
            "FSSAI State License — mandatory for bakeries",
            "Trade license from municipality",
            "GST registration",
            "Pest control certificate — quarterly",
            "Water quality test certificate",
            "If employing staff — Employees' Provident Fund (EPF) if >20 employees",
        ],
        "tips": [
            "Fresh bread smell is your best marketing — keep oven near ventilated entrance",
            "Display birthday cakes prominently — high-value order funnel",
            "Offer same-day custom cakes (4-6 hour order) — premium pricing Rs.600-2000",
            "WhatsApp catalog of cake designs — Rs.500+ orders daily from regular customers",
            "Sell raw dough packs — home baking trend since COVID, unique revenue stream",
        ],
    },
    "hardware": {
        "display_name": "Hardware / Sanitary / Building Materials",
        "min_area": 300,
        "ideal_area": 600,
        "layout_style": "category_zones",
        "customer_flow": "Enter → Browse by category → Counter → Billing",
        "zones": [
            {"id":"electrical","name":"Electrical Section","pct":0.20,"color":"#2d2d0a","icon":"⚡","purpose":"Wires, switches, bulbs, MCBs"},
            {"id":"plumbing","name":"Plumbing & Sanitary","pct":0.22,"color":"#0a1a3d","icon":"🔧","purpose":"Pipes, fittings, taps, basins"},
            {"id":"tools","name":"Tools & Hardware","pct":0.20,"color":"#2d0a0a","icon":"🔨","purpose":"Hand tools, power tools, nails, screws"},
            {"id":"paint","name":"Paint & Chemicals","pct":0.15,"color":"#2d1a0a","icon":"🖌️","purpose":"Paint, primer, adhesives, solvents"},
            {"id":"counter","name":"Counter & Billing","pct":0.12,"color":"#1a0d2d","icon":"💰","purpose":"Payment, invoicing, customer service"},
            {"id":"storage","name":"Bulk Storage / Godown","pct":0.11,"color":"#1a1a2d","icon":"📦","purpose":"Heavy items, bulk stock"},
        ],
        "equipment": [
            {"id":"shelving","name":"Heavy-duty Steel Shelving","w":3,"h":2,"icon":"🗃️","qty":8,"cost":6500,"priority":"essential","notes":"Multiple tiers, labeled by category"},
            {"id":"counter","name":"Sales Counter","w":4,"h":2,"icon":"💰","qty":1,"cost":10000,"priority":"essential","notes":"With glass top for small items"},
            {"id":"computer","name":"Computer + Billing Software","w":0.8,"h":0.5,"icon":"💻","qty":1,"cost":25000,"priority":"essential","notes":"Inventory management + GST billing"},
            {"id":"ladder","name":"Rolling Store Ladder","w":0.5,"h":0.5,"icon":"🪜","qty":2,"cost":3500,"priority":"essential","notes":"For high-shelf access safely"},
            {"id":"weighing","name":"Platform Weighing Scale","w":1,"h":1,"icon":"⚖️","qty":1,"cost":8000,"priority":"recommended","notes":"For loose hardware items"},
            {"id":"forklift_manual","name":"Manual Pallet Jack","w":1,"h":1.5,"icon":"🏗️","qty":1,"cost":12000,"priority":"recommended","notes":"For heavy cement bags, pipes"},
        ],
        "compliance": [
            "Trade license from municipality",
            "GST registration — mandatory for B2B hardware supply",
            "Explosive and Petroleum license if selling gas cylinders / petroleum products",
            "Fire safety — paint and chemicals storage requires fire extinguisher + ventilation",
            "Structural safety for floor loading (heavy materials)",
        ],
        "tips": [
            "Contractor/builder network = 70% of hardware business — build relationships first",
            "Credit to trusted contractors drives loyalty (30-day payment cycle)",
            "Stock fast-moving items: PVC pipe, cement, sand, bricks for construction season",
            "Home delivery to construction sites in 2km — Rs.100 delivery charge, high satisfaction",
            "Plumbing + electrical in one store = one-stop shop advantage over competitors",
        ],
    },
}

class SpaceDesigner:

    def design(self, business_type: str, area_sqft: float, width_ft: float, depth_ft: float, budget: float) -> SpaceDesignResult:
        template = TEMPLATES.get(business_type)
        if not template:
            template = self._generic_template(business_type)

        area = width_ft * depth_ft if (width_ft and depth_ft) else area_sqft
        if not width_ft or not depth_ft:
            ratio = 1.5
            width_ft = math.sqrt(area / ratio)
            depth_ft = area / width_ft

        zones    = self._layout_zones(template, width_ft, depth_ft)
        equip    = self._layout_equipment(template, zones, width_ft, depth_ft, budget)
        costs    = self._estimate_costs(template, area, budget, equip)
        score    = self._efficiency_score(area, template, budget)
        revenue  = self._estimate_revenue(business_type, area)

        return SpaceDesignResult(
            business_type=business_type,
            display_name=template.get("display_name", business_type.replace("_"," ").title()),
            total_area=round(area, 1),
            width_ft=round(width_ft, 1),
            depth_ft=round(depth_ft, 1),
            budget=budget,
            zones=zones,
            equipment=equip,
            cost_breakdown=costs,
            efficiency_score=score,
            compliance_notes=template.get("compliance", []),
            optimization_tips=template.get("tips", []),
            layout_style=template.get("layout_style","standard"),
            customer_flow=template.get("customer_flow","Enter → Browse → Buy → Exit"),
            estimated_setup_cost=costs.get("total_estimated", 0),
            estimated_monthly_revenue=revenue,
        )

    def _layout_zones(self, template: dict, W: float, D: float) -> List[Zone]:
        zone_defs = template.get("zones", [])
        zones: List[Zone] = []
        current_y = 0.0

        for zd in zone_defs:
            pct   = zd["pct"]
            depth = round(D * pct, 1)
            z = Zone(
                id=zd["id"],
                name=zd["name"],
                x=0.0,
                y=round(current_y, 1),
                w=round(W, 1),
                h=depth,
                color=zd["color"],
                icon=zd["icon"],
                pct_of_total=pct,
                purpose=zd["purpose"],
            )
            zones.append(z)
            current_y += depth

        return zones

    def _layout_equipment(self, template: dict, zones: List[Zone], W: float, D: float, budget: float) -> List[Equipment]:
        equip_defs = template.get("equipment", [])
        equipment: List[Equipment] = []
        zone_map = {z.id: z for z in zones}

        placed_positions: List[tuple] = []

        for i, ed in enumerate(equip_defs):
            qty       = ed["qty"]
            unit_cost = ed["cost"]
            total     = qty * unit_cost
            eq_w      = min(ed.get("w", 2), W * 0.4)
            eq_h      = min(ed.get("h", 1.5), D * 0.15)

            x, y = self._find_position(i, ed, zones, zone_map, W, D, placed_positions, eq_w, eq_h)
            placed_positions.append((x, y, eq_w, eq_h))

            equipment.append(Equipment(
                id=ed["id"],
                name=ed["name"],
                x=round(x, 1),
                y=round(y, 1),
                w=round(eq_w, 1),
                h=round(eq_h, 1),
                icon=ed["icon"],
                quantity=qty,
                unit_cost=unit_cost,
                total_cost=total,
                priority=ed.get("priority","essential"),
                notes=ed.get("notes",""),
            ))
        return equipment

    def _find_position(self, index, ed, zones, zone_map, W, D, placed, eq_w, eq_h) -> tuple:
        eq_id = ed["id"]
        # Map equipment to sensible zone locations
        ZONE_HINTS = {
            "counter": ["counter","entrance","reception"],
            "display": ["display","entrance","main_floor","display_area"],
            "refrigerator": ["cold_zone","cold_storage","storage"],
            "workbench": ["workbench","production","repair"],
            "waiting_chairs": ["waiting","reception"],
            "pos": ["counter","reception","entrance"],
            "shelving": ["wall_shelves","main_floor","otc_display"],
        }

        target_zone = None
        for hint_key, zone_ids in ZONE_HINTS.items():
            if hint_key in eq_id:
                for zid in zone_ids:
                    if zid in zone_map:
                        target_zone = zone_map[zid]
                        break
                if target_zone:
                    break

        if not target_zone and zones:
            zi = min(index, len(zones) - 1)
            target_zone = zones[zi]

        if target_zone:
            base_x = 0.5 + (index % 3) * (W / 3)
            base_y = target_zone.y + 0.5 + (index // 3) * (target_zone.h / 4)
            x = min(base_x, W - eq_w - 0.3)
            y = min(base_y, D - eq_h - 0.3)
        else:
            x = 0.5
            y = 0.5 + index * (eq_h + 0.5)

        return max(0.0, x), max(0.0, y)

    def _estimate_costs(self, template: dict, area: float, budget: float, equipment: List[Equipment]) -> dict:
        equip_cost = sum(e.total_cost for e in equipment if e.priority == "essential")
        equip_all  = sum(e.total_cost for e in equipment)

        rent_monthly = area * 30
        interior_cost = area * 350
        electrical    = area * 80
        plumbing      = area * 50
        signage       = 8000
        security_deposit = rent_monthly * 3

        total = equip_cost + interior_cost + electrical + plumbing + signage + security_deposit

        return {
            "equipment_essential": round(equip_cost),
            "equipment_all": round(equip_all),
            "interior_work": round(interior_cost),
            "electrical_wiring": round(electrical),
            "plumbing": round(plumbing),
            "signage_branding": round(signage),
            "security_deposit": round(security_deposit),
            "total_estimated": round(total),
            "budget_gap": round(max(0, total - budget)),
            "budget_utilization_pct": round(min(100, total / max(budget, 1) * 100), 1),
            "monthly_rent_estimate": round(rent_monthly),
        }

    def _efficiency_score(self, area: float, template: dict, budget: float) -> float:
        ideal   = template.get("ideal_area", 400)
        min_area= template.get("min_area", 100)
        area_score = max(0, min(1, (area - min_area) / (ideal - min_area + 1))) * 40
        budget_score = min(40, (budget / 200000) * 40)
        base_score = 20
        return round(area_score + budget_score + base_score, 1)

    def _estimate_revenue(self, business_type: str, area: float) -> float:
        base = {
            "grocery": 120000, "pharmacy": 80000, "salon": 60000,
            "restaurant": 150000, "cafe": 100000, "gym": 200000,
            "clinic": 250000, "school": 500000, "coaching": 80000,
            "hardware": 100000, "mobile_repair": 40000, "bakery": 60000,
            "tea_stall": 20000, "vegetable_vendor": 25000,
        }.get(business_type, 50000)
        size_multiplier = min(2.0, max(0.5, area / 300))
        return round(base * size_multiplier)

    def _generic_template(self, business_type: str) -> dict:
        return {
            "display_name": business_type.replace("_"," ").title(),
            "min_area": 150,
            "ideal_area": 300,
            "layout_style": "standard",
            "customer_flow": "Enter → Browse → Purchase → Exit",
            "zones": [
                {"id":"entrance","name":"Entrance","pct":0.08,"color":"#1a2d2d","icon":"🚪","purpose":"Entry and visibility"},
                {"id":"main","name":"Main Area","pct":0.60,"color":"#0d1a2d","icon":"🏪","purpose":"Core business activity"},
                {"id":"counter","name":"Counter","pct":0.12,"color":"#2d1a0a","icon":"💰","purpose":"Transaction and service"},
                {"id":"storage","name":"Storage","pct":0.15,"color":"#1a1a2d","icon":"📦","purpose":"Stock and supplies"},
                {"id":"utilities","name":"Utilities","pct":0.05,"color":"#1a2a1a","icon":"🔌","purpose":"Power, plumbing, WC"},
            ],
            "equipment": [
                {"id":"counter","name":"Service Counter","w":3,"h":2,"icon":"🪑","qty":1,"cost":8000,"priority":"essential","notes":"Main customer interface"},
                {"id":"shelving","name":"Storage Shelf","w":3,"h":2,"icon":"📦","qty":3,"cost":3500,"priority":"essential","notes":"Organized storage"},
                {"id":"pos","name":"POS Terminal","w":0.5,"h":0.5,"icon":"📟","qty":1,"cost":8000,"priority":"recommended","notes":"Digital billing"},
            ],
            "compliance": [
                "Trade license from local municipality",
                "Shop and Establishment Act certificate",
                "GST registration if revenue > Rs.20 lakh",
            ],
            "tips": [
                "Keep the entrance clean and visible from the road",
                "Good lighting increases customer dwell time and sales",
                "Digital payment options increase average transaction value",
            ],
        }

    def list_business_types(self) -> List[dict]:
        return [{"type": k, "display_name": v["display_name"], "min_area": v.get("min_area",100), "ideal_area": v.get("ideal_area",300)} for k, v in TEMPLATES.items()]
