"""
SPANDAN AI — Comprehensive India Pincode Database
Covers all 28 states + major UTs, 400+ pincodes.

Format per entry:
  city, district, state, lat, lng, population, avg_income(annual ₹), age_dominant, tier
  tier: metro | tier1 | tier2 | tier3
  age_dominant: youth | working | family
"""

from typing import TypedDict, Optional, List

class PincodeEntry(TypedDict):
    city: str
    district: str
    state: str
    lat: float
    lng: float
    population: int
    avg_income: int
    age_dominant: str
    tier: str
    literacy_rate: float
    commercial_density: float

# ────────────────────────────────────────────────────────────────────
# Raw data: (city, district, state, lat, lng, pop, income, age, tier, literacy, density)
# ────────────────────────────────────────────────────────────────────
_RAW: list = [

    # ── KARNATAKA ────────────────────────────────────────────────────
    ("560001","Bangalore Central","Bangalore Urban","Karnataka",12.9716,77.5946,45000,850000,"working","metro",0.93,0.82),
    ("560002","Shivajinagar","Bangalore Urban","Karnataka",12.9850,77.6010,38000,780000,"working","metro",0.92,0.75),
    ("560003","Sadashivanagar","Bangalore Urban","Karnataka",13.0125,77.5775,42000,1400000,"working","metro",0.96,0.55),
    ("560004","Rajajinagar","Bangalore Urban","Karnataka",12.9983,77.5520,55000,820000,"family","metro",0.91,0.68),
    ("560008","Malleswaram","Bangalore Urban","Karnataka",13.0035,77.5680,60000,1100000,"family","metro",0.94,0.72),
    ("560010","Gandhinagar","Bangalore Urban","Karnataka",12.9762,77.5721,50000,750000,"working","metro",0.91,0.80),
    ("560011","Vijayanagar","Bangalore Urban","Karnataka",12.9675,77.5320,75000,680000,"family","metro",0.89,0.65),
    ("560012","Nagarbhavi","Bangalore Urban","Karnataka",12.9537,77.5058,68000,600000,"youth","metro",0.87,0.58),
    ("560016","Banashankari","Bangalore Urban","Karnataka",12.9337,77.5467,82000,720000,"family","metro",0.90,0.62),
    ("560019","Jayanagar","Bangalore Urban","Karnataka",12.9250,77.5823,95000,950000,"family","metro",0.93,0.70),
    ("560025","BTM Layout","Bangalore Urban","Karnataka",12.9165,77.6101,110000,870000,"youth","metro",0.91,0.72),
    ("560029","JP Nagar","Bangalore Urban","Karnataka",12.9063,77.5932,125000,900000,"family","metro",0.92,0.68),
    ("560034","HSR Layout","Bangalore Urban","Karnataka",12.9082,77.6476,95000,1300000,"youth","metro",0.94,0.65),
    ("560037","Whitefield","Bangalore Urban","Karnataka",12.9698,77.7500,85000,1200000,"working","metro",0.93,0.60),
    ("560038","Marathahalli","Bangalore Urban","Karnataka",12.9592,77.6975,92000,1100000,"youth","metro",0.92,0.68),
    ("560041","Koramangala","Bangalore Urban","Karnataka",12.9352,77.6244,80000,1500000,"youth","metro",0.95,0.75),
    ("560064","Indiranagar","Bangalore Urban","Karnataka",12.9784,77.6408,70000,1600000,"youth","metro",0.96,0.80),
    ("560066","Hebbal","Bangalore Urban","Karnataka",13.0358,77.5970,120000,950000,"family","metro",0.91,0.62),
    ("560068","Bellandur","Bangalore Urban","Karnataka",12.9253,77.6764,70000,1400000,"youth","metro",0.94,0.58),
    ("560078","Sarjapur Road","Bangalore Urban","Karnataka",12.9010,77.6887,88000,1250000,"working","metro",0.93,0.60),
    ("560095","Kengeri","Bangalore Urban","Karnataka",12.9051,77.4834,72000,560000,"family","metro",0.86,0.55),
    ("560100","Electronic City","Bangalore Urban","Karnataka",12.8399,77.6770,95000,750000,"working","metro",0.90,0.62),
    ("560103","Yelahanka","Bangalore North","Karnataka",13.1005,77.5962,78000,680000,"family","metro",0.88,0.58),
    ("560114","Bannerghatta","Bangalore South","Karnataka",12.8640,77.5966,55000,520000,"family","tier2",0.84,0.45),
    # Mysore
    ("570001","Mysore City","Mysuru","Karnataka",12.3051,76.6551,95000,580000,"working","tier1",0.89,0.70),
    ("570002","Mysore West","Mysuru","Karnataka",12.2958,76.6394,82000,520000,"family","tier1",0.87,0.62),
    ("570008","Saraswatipuram","Mysuru","Karnataka",12.3251,76.6368,65000,680000,"family","tier1",0.91,0.58),
    ("570010","Kuvempunagar","Mysuru","Karnataka",12.3108,76.6215,72000,620000,"youth","tier1",0.90,0.60),
    # Hubli-Dharwad
    ("580001","Hubli","Dharwad","Karnataka",15.3647,75.1240,110000,520000,"working","tier2",0.82,0.68),
    ("580020","Vidyanagar Hubli","Dharwad","Karnataka",15.3576,75.1353,88000,580000,"youth","tier2",0.85,0.60),
    ("580032","Dharwad","Dharwad","Karnataka",15.4589,75.0078,72000,500000,"working","tier2",0.84,0.62),
    # Mangalore
    ("575001","Mangalore City","Dakshina Kannada","Karnataka",12.8701,74.8428,90000,620000,"working","tier1",0.91,0.72),
    ("575002","Hampankatta","Dakshina Kannada","Karnataka",12.8720,74.8418,78000,580000,"working","tier1",0.90,0.75),
    ("575006","Mangalore South","Dakshina Kannada","Karnataka",12.8450,74.8620,65000,540000,"family","tier1",0.89,0.60),
    # Belgaum/Belagavi
    ("590001","Belagavi","Belagavi","Karnataka",15.8497,74.4977,85000,480000,"working","tier2",0.82,0.65),
    ("590006","Belagavi South","Belagavi","Karnataka",15.8320,74.5020,68000,440000,"family","tier2",0.80,0.55),
    # Davangere
    ("577001","Davangere","Davangere","Karnataka",14.4644,75.9218,80000,450000,"working","tier2",0.80,0.60),
    # Shimoga
    ("577201","Shimoga","Shivamogga","Karnataka",13.9299,75.5681,70000,470000,"working","tier2",0.82,0.58),

    # ── MAHARASHTRA ───────────────────────────────────────────────────
    # Mumbai
    ("400001","Mumbai Fort","Mumbai","Maharashtra",18.9388,72.8354,65000,900000,"working","metro",0.92,0.85),
    ("400002","Masjid Bunder","Mumbai","Maharashtra",18.9465,72.8406,72000,650000,"working","metro",0.88,0.80),
    ("400005","Colaba","Mumbai","Maharashtra",18.9067,72.8147,55000,1800000,"working","metro",0.94,0.78),
    ("400012","Parel","Mumbai","Maharashtra",18.9976,72.8376,85000,850000,"working","metro",0.91,0.75),
    ("400013","Dadar","Mumbai","Maharashtra",19.0176,72.8496,90000,780000,"family","metro",0.90,0.80),
    ("400016","Mahim","Mumbai","Maharashtra",19.0376,72.8400,75000,820000,"family","metro",0.90,0.72),
    ("400018","Worli","Mumbai","Maharashtra",19.0138,72.8168,70000,1500000,"working","metro",0.92,0.70),
    ("400025","Bandra West","Mumbai Suburban","Maharashtra",19.0596,72.8295,68000,2000000,"youth","metro",0.95,0.78),
    ("400050","Bandra East","Mumbai Suburban","Maharashtra",19.0681,72.8442,74000,1100000,"working","metro",0.93,0.72),
    ("400051","Santacruz","Mumbai Suburban","Maharashtra",19.0833,72.8385,80000,980000,"family","metro",0.92,0.68),
    ("400053","Andheri West","Mumbai Suburban","Maharashtra",19.1197,72.8464,110000,950000,"youth","metro",0.91,0.72),
    ("400059","Andheri East","Mumbai Suburban","Maharashtra",19.1136,72.8697,125000,1050000,"working","metro",0.92,0.75),
    ("400063","Borivali","Mumbai Suburban","Maharashtra",19.2307,72.8567,135000,720000,"family","metro",0.90,0.65),
    ("400066","Kandivali","Mumbai Suburban","Maharashtra",19.2041,72.8601,128000,680000,"family","metro",0.89,0.62),
    ("400069","Malad","Mumbai Suburban","Maharashtra",19.1863,72.8484,140000,750000,"working","metro",0.90,0.68),
    ("400072","Chembur","Mumbai Suburban","Maharashtra",19.0633,72.8993,118000,820000,"family","metro",0.91,0.70),
    ("400080","Ghatkopar","Mumbai Suburban","Maharashtra",19.0863,72.9083,118000,680000,"family","metro",0.90,0.68),
    ("400092","Powai","Mumbai Suburban","Maharashtra",19.1176,72.9060,90000,1400000,"youth","metro",0.94,0.65),
    ("400093","Mulund","Mumbai Suburban","Maharashtra",19.1726,72.9491,100000,780000,"family","metro",0.91,0.62),
    # Pune
    ("411001","Pune Camp","Pune","Maharashtra",18.5204,73.8567,72000,900000,"working","metro",0.93,0.80),
    ("411002","Shivajinagar","Pune","Maharashtra",18.5314,73.8446,68000,1100000,"youth","metro",0.94,0.75),
    ("411004","Deccan","Pune","Maharashtra",18.5176,73.8391,85000,980000,"youth","metro",0.93,0.72),
    ("411007","Aundh","Pune","Maharashtra",18.5579,73.8079,90000,1050000,"family","metro",0.92,0.65),
    ("411014","Kothrud","Pune","Maharashtra",18.4994,73.8078,120000,850000,"family","metro",0.91,0.62),
    ("411021","Hadapsar","Pune","Maharashtra",18.5018,73.9260,145000,750000,"working","metro",0.89,0.68),
    ("411045","Viman Nagar","Pune","Maharashtra",18.5679,73.9143,78000,1300000,"youth","metro",0.94,0.68),
    ("411048","Baner","Pune","Maharashtra",18.5611,73.7875,88000,1400000,"youth","metro",0.95,0.65),
    ("411057","Hinjewadi","Pune","Maharashtra",18.5912,73.7380,95000,1100000,"youth","metro",0.93,0.58),
    # Nagpur
    ("440001","Nagpur Central","Nagpur","Maharashtra",21.1458,79.0882,85000,580000,"working","tier2",0.87,0.72),
    ("440002","Dharampeth","Nagpur","Maharashtra",21.1434,79.0680,78000,720000,"working","tier2",0.90,0.68),
    ("440009","Sadar Nagpur","Nagpur","Maharashtra",21.1504,79.0750,72000,680000,"family","tier2",0.88,0.65),
    ("440015","Manewada","Nagpur","Maharashtra",21.1225,79.1005,65000,500000,"family","tier2",0.84,0.55),
    # Nashik
    ("422001","Nashik City","Nashik","Maharashtra",19.9975,73.7898,92000,580000,"working","tier2",0.86,0.68),
    ("422002","Nashik Road","Nashik","Maharashtra",19.9822,73.8207,82000,540000,"working","tier2",0.84,0.62),
    # Aurangabad/Chhatrapati Sambhajinagar
    ("431001","Aurangabad City","Aurangabad","Maharashtra",19.8762,75.3433,88000,560000,"working","tier2",0.82,0.65),
    # Thane
    ("400601","Thane West","Thane","Maharashtra",19.1853,72.9781,120000,820000,"family","metro",0.91,0.68),
    ("400602","Thane East","Thane","Maharashtra",19.2018,73.0083,110000,750000,"family","metro",0.90,0.62),
    # Kolhapur
    ("416001","Kolhapur","Kolhapur","Maharashtra",16.7050,74.2433,85000,550000,"working","tier2",0.85,0.65),
    # Solapur
    ("413001","Solapur","Solapur","Maharashtra",17.6805,75.9064,90000,480000,"working","tier2",0.81,0.60),

    # ── DELHI NCR ─────────────────────────────────────────────────────
    ("110001","Connaught Place","Central Delhi","Delhi",28.6315,77.2167,55000,700000,"youth","metro",0.93,0.88),
    ("110005","Karol Bagh","Central Delhi","Delhi",28.6514,77.1907,80000,600000,"family","metro",0.91,0.85),
    ("110006","Paharganj","Central Delhi","Delhi",28.6462,77.2135,70000,450000,"working","metro",0.88,0.82),
    ("110007","New Delhi","New Delhi","Delhi",28.6139,77.2090,65000,850000,"working","metro",0.93,0.78),
    ("110008","Patel Nagar","West Delhi","Delhi",28.6520,77.1604,88000,680000,"working","metro",0.90,0.75),
    ("110016","Hauz Khas","South Delhi","Delhi",28.5431,77.2040,65000,1500000,"youth","metro",0.95,0.78),
    ("110017","Saket","South Delhi","Delhi",28.5244,77.2066,78000,1200000,"family","metro",0.93,0.72),
    ("110019","Kalkaji","South East Delhi","Delhi",28.5392,77.2527,82000,750000,"family","metro",0.90,0.70),
    ("110020","Okhla","South East Delhi","Delhi",28.5355,77.2710,90000,620000,"working","metro",0.88,0.75),
    ("110025","Lajpat Nagar","South Delhi","Delhi",28.5706,77.2403,95000,850000,"working","metro",0.92,0.80),
    ("110029","Vasant Kunj","South West Delhi","Delhi",28.5230,77.1588,72000,1300000,"youth","metro",0.94,0.65),
    ("110044","Govindpuri","South East Delhi","Delhi",28.5310,77.2755,98000,520000,"working","metro",0.87,0.70),
    ("110048","Vasant Vihar","South West Delhi","Delhi",28.5590,77.1625,60000,2500000,"working","metro",0.96,0.60),
    ("110049","Malviya Nagar","South Delhi","Delhi",28.5298,77.1952,72000,1000000,"youth","metro",0.93,0.68),
    ("110058","Janakpuri","West Delhi","Delhi",28.6252,77.0832,110000,680000,"family","metro",0.90,0.65),
    ("110062","Dwarka","South West Delhi","Delhi",28.5921,77.0460,145000,720000,"family","metro",0.91,0.62),
    ("110075","Rohini","North West Delhi","Delhi",28.7216,77.1130,160000,650000,"family","metro",0.89,0.62),
    ("110085","Shalimar Bagh","North West Delhi","Delhi",28.7139,77.1623,120000,680000,"family","metro",0.90,0.65),
    ("110091","Patparganj","East Delhi","Delhi",28.6153,77.2952,95000,780000,"working","metro",0.91,0.72),
    ("110092","Mayur Vihar","East Delhi","Delhi",28.6062,77.2972,105000,720000,"family","metro",0.91,0.68),
    # Gurgaon
    ("122001","Gurgaon City","Gurgaon","Haryana",28.4595,77.0266,110000,1200000,"working","metro",0.92,0.80),
    ("122002","DLF Cyber City","Gurgaon","Haryana",28.4943,77.0882,88000,2000000,"youth","metro",0.96,0.72),
    ("122008","Manesar","Gurgaon","Haryana",28.3588,76.9362,75000,780000,"working","metro",0.88,0.65),
    ("122018","Sohna Road","Gurgaon","Haryana",28.4143,77.0368,65000,1400000,"youth","metro",0.93,0.62),
    # Noida
    ("201301","Noida Sector 1","Gautam Buddha Nagar","Uttar Pradesh",28.5355,77.3910,95000,900000,"working","metro",0.92,0.70),
    ("201305","Noida Sector 18","Gautam Buddha Nagar","Uttar Pradesh",28.5700,77.3200,88000,1100000,"youth","metro",0.94,0.78),
    ("201307","Greater Noida","Gautam Buddha Nagar","Uttar Pradesh",28.4744,77.5040,110000,850000,"working","metro",0.91,0.65),

    # ── TELANGANA ─────────────────────────────────────────────────────
    ("500001","Hyderabad Central","Hyderabad","Telangana",17.3850,78.4867,75000,850000,"working","metro",0.88,0.82),
    ("500003","Secunderabad","Secunderabad","Telangana",17.4399,78.4983,88000,780000,"working","metro",0.88,0.78),
    ("500004","Abids","Hyderabad","Telangana",17.3894,78.4741,70000,700000,"working","metro",0.87,0.80),
    ("500008","Nampally","Hyderabad","Telangana",17.3942,78.4690,68000,620000,"family","metro",0.86,0.72),
    ("500016","Himayathnagar","Hyderabad","Telangana",17.4062,78.4767,70000,1100000,"youth","metro",0.91,0.75),
    ("500018","Banjara Hills","Hyderabad","Telangana",17.4126,78.4475,55000,2200000,"working","metro",0.94,0.72),
    ("500026","Ameerpet","Hyderabad","Telangana",17.4367,78.4489,85000,950000,"youth","metro",0.91,0.80),
    ("500034","Jubilee Hills","Hyderabad","Telangana",17.4329,78.4072,58000,2500000,"working","metro",0.95,0.68),
    ("500038","Madhapur","Hyderabad","Telangana",17.4485,78.3908,85000,1400000,"youth","metro",0.93,0.72),
    ("500045","Begumpet","Secunderabad","Telangana",17.4481,78.4657,72000,1200000,"working","metro",0.92,0.75),
    ("500072","Gachibowli","Hyderabad","Telangana",17.4401,78.3489,78000,1600000,"youth","metro",0.94,0.68),
    ("500081","HITEC City","Hyderabad","Telangana",17.4476,78.3760,72000,1800000,"youth","metro",0.95,0.65),
    ("500084","Kukatpally","Hyderabad","Telangana",17.4849,78.3995,125000,780000,"family","metro",0.90,0.68),
    ("500090","LB Nagar","Hyderabad","Telangana",17.3464,78.5526,108000,650000,"family","metro",0.88,0.65),
    # Warangal
    ("506001","Warangal","Warangal","Telangana",17.9784,79.5941,88000,480000,"working","tier2",0.82,0.65),
    ("506002","Hanamkonda","Warangal","Telangana",18.0050,79.5630,72000,460000,"working","tier2",0.81,0.60),
    # Karimnagar
    ("505001","Karimnagar","Karimnagar","Telangana",18.4386,79.1288,65000,430000,"working","tier2",0.80,0.58),

    # ── TAMIL NADU ────────────────────────────────────────────────────
    ("600001","Chennai Central","Chennai","Tamil Nadu",13.0827,80.2707,60000,780000,"family","metro",0.90,0.82),
    ("600002","Parry's Corner","Chennai","Tamil Nadu",13.0878,80.2866,55000,700000,"working","metro",0.89,0.85),
    ("600004","Nungambakkam","Chennai","Tamil Nadu",13.0569,80.2425,65000,1500000,"working","metro",0.94,0.78),
    ("600006","Egmore","Chennai","Tamil Nadu",13.0732,80.2609,70000,700000,"working","metro",0.91,0.80),
    ("600010","Guindy","Chennai","Tamil Nadu",13.0067,80.2207,78000,950000,"working","metro",0.91,0.72),
    ("600014","Kodambakkam","Chennai","Tamil Nadu",13.0500,80.2231,88000,850000,"family","metro",0.90,0.75),
    ("600017","T Nagar","Chennai","Tamil Nadu",13.0418,80.2341,95000,1200000,"family","metro",0.92,0.85),
    ("600020","Adyar","Chennai","Tamil Nadu",13.0012,80.2565,80000,1400000,"working","metro",0.93,0.72),
    ("600028","Arumbakkam","Chennai","Tamil Nadu",13.0800,80.2078,88000,750000,"family","metro",0.90,0.68),
    ("600032","Velachery","Chennai","Tamil Nadu",12.9750,80.2200,105000,950000,"family","metro",0.91,0.70),
    ("600040","Anna Nagar","Chennai","Tamil Nadu",13.0854,80.2101,110000,1100000,"family","metro",0.92,0.72),
    ("600041","Ambattur","Tiruvallur","Tamil Nadu",13.1143,80.1548,130000,650000,"working","metro",0.88,0.65),
    ("600042","Avadi","Tiruvallur","Tamil Nadu",13.1069,80.1056,115000,580000,"working","tier1",0.86,0.60),
    # Coimbatore
    ("641001","Coimbatore","Coimbatore","Tamil Nadu",11.0168,76.9558,95000,620000,"working","tier1",0.88,0.72),
    ("641004","RS Puram","Coimbatore","Tamil Nadu",11.0104,76.9593,85000,750000,"family","tier1",0.90,0.68),
    ("641011","Peelamedu","Coimbatore","Tamil Nadu",11.0220,77.0174,78000,820000,"youth","tier1",0.89,0.62),
    ("641018","Singanallur","Coimbatore","Tamil Nadu",10.9983,77.0166,70000,680000,"working","tier1",0.87,0.60),
    # Madurai
    ("625001","Madurai City","Madurai","Tamil Nadu",9.9252,78.1198,88000,550000,"working","tier1",0.86,0.72),
    ("625002","Madurai North","Madurai","Tamil Nadu",9.9500,78.1300,78000,510000,"family","tier1",0.84,0.65),
    ("625011","Madurai South","Madurai","Tamil Nadu",9.9120,78.1230,72000,480000,"family","tier1",0.83,0.60),
    # Trichy
    ("620001","Trichy","Tiruchirappalli","Tamil Nadu",10.7905,78.7047,80000,520000,"working","tier1",0.87,0.65),
    ("620002","Thiruverumbur","Tiruchirappalli","Tamil Nadu",10.8253,78.7338,68000,480000,"working","tier1",0.85,0.58),
    # Salem
    ("636001","Salem","Salem","Tamil Nadu",11.6643,78.1460,88000,520000,"working","tier2",0.85,0.65),
    # Tirunelveli
    ("627001","Tirunelveli","Tirunelveli","Tamil Nadu",8.7139,77.7567,78000,490000,"working","tier2",0.86,0.62),
    # Erode
    ("638001","Erode","Erode","Tamil Nadu",11.3410,77.7172,72000,560000,"working","tier2",0.85,0.62),

    # ── UTTAR PRADESH ─────────────────────────────────────────────────
    ("226001","Lucknow Hazratganj","Lucknow","Uttar Pradesh",26.8467,80.9462,92000,520000,"working","tier1",0.83,0.78),
    ("226002","Lucknow Chowk","Lucknow","Uttar Pradesh",26.8590,80.9248,88000,480000,"working","tier1",0.81,0.75),
    ("226003","Lucknow Alambagh","Lucknow","Uttar Pradesh",26.8079,80.9261,85000,480000,"family","tier1",0.80,0.65),
    ("226010","Gomtinagar","Lucknow","Uttar Pradesh",26.8605,81.0129,85000,750000,"youth","tier1",0.87,0.72),
    ("226012","Aliganj","Lucknow","Uttar Pradesh",26.8968,80.9624,78000,650000,"family","tier1",0.85,0.65),
    ("226016","Vikas Nagar","Lucknow","Uttar Pradesh",26.8754,80.9813,72000,580000,"family","tier1",0.83,0.60),
    ("226022","Indira Nagar","Lucknow","Uttar Pradesh",26.8962,81.0022,80000,680000,"youth","tier1",0.86,0.68),
    # Kanpur
    ("208001","Kanpur City","Kanpur","Uttar Pradesh",26.4499,80.3319,95000,500000,"working","tier1",0.79,0.72),
    ("208002","Kidwai Nagar","Kanpur","Uttar Pradesh",26.4603,80.3400,88000,560000,"working","tier1",0.81,0.68),
    ("208012","Govindnagar","Kanpur","Uttar Pradesh",26.4721,80.3491,80000,520000,"family","tier1",0.80,0.62),
    ("208020","Kakadeo","Kanpur","Uttar Pradesh",26.4875,80.2957,72000,600000,"youth","tier1",0.83,0.62),
    # Agra
    ("282001","Agra City","Agra","Uttar Pradesh",27.1767,78.0081,88000,500000,"working","tier1",0.78,0.75),
    ("282002","Agra Civil Lines","Agra","Uttar Pradesh",27.2007,78.0072,78000,620000,"working","tier1",0.82,0.68),
    ("282005","Taj Ganj","Agra","Uttar Pradesh",27.1707,78.0365,65000,450000,"working","tier1",0.76,0.72),
    # Varanasi
    ("221001","Varanasi City","Varanasi","Uttar Pradesh",25.3176,82.9739,92000,480000,"working","tier1",0.80,0.78),
    ("221002","Varanasi Assi","Varanasi","Uttar Pradesh",25.2919,83.0149,78000,520000,"youth","tier1",0.82,0.68),
    ("221005","Varanasi Sigra","Varanasi","Uttar Pradesh",25.3345,82.9825,85000,540000,"family","tier1",0.81,0.65),
    # Allahabad/Prayagraj
    ("211001","Prayagraj City","Prayagraj","Uttar Pradesh",25.4358,81.8463,95000,490000,"working","tier1",0.81,0.72),
    ("211002","Civil Lines","Prayagraj","Uttar Pradesh",25.4591,81.8476,80000,650000,"working","tier1",0.85,0.65),
    # Meerut
    ("250001","Meerut City","Meerut","Uttar Pradesh",28.9845,77.7064,108000,520000,"working","tier1",0.79,0.70),
    ("250004","Meerut Cantonment","Meerut","Uttar Pradesh",29.0095,77.6980,72000,680000,"working","tier1",0.83,0.62),
    # Ghaziabad
    ("201001","Ghaziabad","Ghaziabad","Uttar Pradesh",28.6692,77.4538,128000,650000,"working","metro",0.87,0.72),
    ("201011","Indirapuram","Ghaziabad","Uttar Pradesh",28.6468,77.3653,115000,850000,"youth","metro",0.90,0.68),
    # Mathura
    ("281001","Mathura","Mathura","Uttar Pradesh",27.4924,77.6737,75000,440000,"working","tier2",0.77,0.65),

    # ── GUJARAT ───────────────────────────────────────────────────────
    ("380001","Ahmedabad Central","Ahmedabad","Gujarat",23.0225,72.5714,80000,720000,"working","metro",0.88,0.82),
    ("380002","Ahmedabad Paldi","Ahmedabad","Gujarat",23.0081,72.5665,75000,680000,"family","metro",0.87,0.72),
    ("380004","Maninagar","Ahmedabad","Gujarat",22.9939,72.6076,110000,650000,"family","metro",0.86,0.70),
    ("380006","Navrangpura","Ahmedabad","Gujarat",23.0368,72.5570,75000,1100000,"youth","metro",0.91,0.78),
    ("380009","Vastrapur","Ahmedabad","Gujarat",23.0358,72.5271,85000,1300000,"family","metro",0.92,0.72),
    ("380015","Naroda","Ahmedabad","Gujarat",23.0752,72.6391,90000,580000,"working","metro",0.84,0.65),
    ("380021","Bopal","Ahmedabad","Gujarat",23.0219,72.4616,78000,1200000,"youth","metro",0.91,0.60),
    ("380054","Satellite","Ahmedabad","Gujarat",23.0245,72.5080,92000,1500000,"youth","metro",0.93,0.75),
    ("380060","Bodakdev","Ahmedabad","Gujarat",23.0470,72.5150,82000,1600000,"youth","metro",0.93,0.72),
    # Surat
    ("395001","Surat Central","Surat","Gujarat",21.1953,72.8326,98000,680000,"working","metro",0.86,0.78),
    ("395002","Athwa","Surat","Gujarat",21.1891,72.8266,88000,780000,"family","metro",0.88,0.72),
    ("395006","Katargam","Surat","Gujarat",21.2224,72.8484,105000,620000,"working","metro",0.84,0.68),
    ("395009","Vesu","Surat","Gujarat",21.1514,72.7893,82000,950000,"youth","metro",0.89,0.62),
    ("395023","Althan","Surat","Gujarat",21.1583,72.8082,72000,1000000,"youth","metro",0.90,0.58),
    # Vadodara
    ("390001","Vadodara City","Vadodara","Gujarat",22.3072,73.1812,88000,680000,"working","tier1",0.88,0.75),
    ("390007","Karelibaug","Vadodara","Gujarat",22.3232,73.2082,80000,620000,"family","tier1",0.87,0.68),
    ("390011","Alkapuri","Vadodara","Gujarat",22.2970,73.1791,72000,1000000,"youth","tier1",0.91,0.70),
    ("390015","Akota","Vadodara","Gujarat",22.3015,73.1550,68000,800000,"family","tier1",0.89,0.62),
    # Rajkot
    ("360001","Rajkot City","Rajkot","Gujarat",22.3039,70.8022,92000,580000,"working","tier1",0.86,0.70),
    ("360002","Rajkot Gondal Road","Rajkot","Gujarat",22.2800,70.7800,78000,620000,"family","tier1",0.85,0.62),
    ("360005","Bhaktinagar","Rajkot","Gujarat",22.3150,70.8250,65000,560000,"youth","tier1",0.84,0.58),

    # ── RAJASTHAN ─────────────────────────────────────────────────────
    ("302001","Jaipur Central","Jaipur","Rajasthan",26.9124,75.7873,88000,580000,"working","tier1",0.82,0.78),
    ("302002","Jaipur Civil Lines","Jaipur","Rajasthan",26.9224,75.8035,80000,720000,"working","tier1",0.85,0.72),
    ("302004","Bani Park","Jaipur","Rajasthan",26.9267,75.7913,72000,850000,"family","tier1",0.87,0.68),
    ("302006","Malviya Nagar Jaipur","Jaipur","Rajasthan",26.8581,75.8124,75000,680000,"family","tier1",0.84,0.65),
    ("302012","Vaishali Nagar","Jaipur","Rajasthan",26.9137,75.7308,85000,750000,"youth","tier1",0.86,0.68),
    ("302019","Mansarovar","Jaipur","Rajasthan",26.8601,75.7636,92000,680000,"family","tier1",0.84,0.62),
    ("302020","Pratap Nagar","Jaipur","Rajasthan",26.8432,75.8285,78000,600000,"youth","tier1",0.83,0.60),
    ("302039","Jagatpura","Jaipur","Rajasthan",26.8268,75.8474,68000,580000,"working","tier1",0.82,0.58),
    # Jodhpur
    ("342001","Jodhpur City","Jodhpur","Rajasthan",26.2389,73.0243,78000,480000,"working","tier2",0.79,0.70),
    ("342003","Sardarpura","Jodhpur","Rajasthan",26.2400,73.0100,70000,540000,"working","tier2",0.81,0.65),
    ("342005","Basni","Jodhpur","Rajasthan",26.2200,72.9800,65000,500000,"family","tier2",0.78,0.58),
    # Udaipur
    ("313001","Udaipur City","Udaipur","Rajasthan",24.5854,73.7125,72000,520000,"working","tier2",0.81,0.68),
    ("313002","Fatehpura","Udaipur","Rajasthan",24.5760,73.6920,62000,480000,"family","tier2",0.79,0.60),
    # Kota
    ("324001","Kota City","Kota","Rajasthan",25.2138,75.8648,78000,500000,"youth","tier2",0.82,0.68),
    ("324002","Kota Talwandi","Kota","Rajasthan",25.1980,75.8500,65000,540000,"youth","tier2",0.83,0.62),
    # Ajmer
    ("305001","Ajmer","Ajmer","Rajasthan",26.4499,74.6399,72000,450000,"working","tier2",0.78,0.65),

    # ── WEST BENGAL ───────────────────────────────────────────────────
    ("700001","Kolkata BBD Bagh","Kolkata","West Bengal",22.5726,88.3639,78000,600000,"working","metro",0.88,0.82),
    ("700006","Park Street","Kolkata","West Bengal",22.5524,88.3527,65000,1200000,"working","metro",0.93,0.78),
    ("700007","Bhowanipore","Kolkata","West Bengal",22.5297,88.3438,70000,900000,"family","metro",0.90,0.72),
    ("700014","Kalighat","Kolkata","West Bengal",22.5229,88.3428,68000,780000,"family","metro",0.89,0.70),
    ("700019","Ballygunge","Kolkata","West Bengal",22.5280,88.3680,72000,1100000,"working","metro",0.92,0.72),
    ("700025","Gariahat","Kolkata","West Bengal",22.5170,88.3649,75000,1000000,"family","metro",0.91,0.78),
    ("700026","Deshapriya Park","Kolkata","West Bengal",22.5210,88.3550,68000,950000,"family","metro",0.91,0.72),
    ("700027","Alipore","Kolkata","West Bengal",22.5307,88.3378,62000,1500000,"working","metro",0.94,0.65),
    ("700032","Behala","Kolkata","West Bengal",22.4961,88.3082,110000,580000,"family","metro",0.87,0.65),
    ("700052","Salt Lake","North 24 Parganas","West Bengal",22.5958,88.4155,85000,1000000,"youth","metro",0.93,0.68),
    ("700091","New Town","North 24 Parganas","West Bengal",22.5925,88.4823,88000,1000000,"youth","metro",0.93,0.65),
    ("700156","Action Area","North 24 Parganas","West Bengal",22.5640,88.4520,72000,1200000,"youth","metro",0.94,0.60),
    # Howrah
    ("711101","Howrah City","Howrah","West Bengal",22.5958,88.2636,95000,500000,"working","metro",0.84,0.72),
    ("711106","Howrah Shibpur","Howrah","West Bengal",22.5779,88.3022,82000,520000,"working","metro",0.85,0.68),
    # Durgapur
    ("713201","Durgapur City","Paschim Bardhaman","West Bengal",23.5204,87.3119,85000,540000,"working","tier2",0.83,0.65),
    # Siliguri
    ("734001","Siliguri","Darjeeling","West Bengal",26.7271,88.3953,88000,520000,"working","tier2",0.82,0.70),
    ("734006","Siliguri Hakimpara","Darjeeling","West Bengal",26.7100,88.4200,72000,480000,"family","tier2",0.80,0.62),
    # Asansol
    ("713301","Asansol","Paschim Bardhaman","West Bengal",23.6800,86.9700,80000,490000,"working","tier2",0.81,0.62),

    # ── PUNJAB & HARYANA ─────────────────────────────────────────────
    ("160001","Chandigarh Sector 1","Chandigarh","Chandigarh",30.7333,76.7794,62000,900000,"youth","tier1",0.94,0.75),
    ("160017","Chandigarh Sector 17","Chandigarh","Chandigarh",30.7421,76.7874,58000,1000000,"working","tier1",0.95,0.80),
    ("160019","Chandigarh Sector 35","Chandigarh","Chandigarh",30.7249,76.7793,65000,850000,"family","tier1",0.93,0.68),
    ("160022","Chandigarh Sector 43","Chandigarh","Chandigarh",30.7062,76.7864,72000,920000,"working","tier1",0.93,0.65),
    # Ludhiana
    ("141001","Ludhiana City","Ludhiana","Punjab",30.9010,75.8573,108000,650000,"working","tier1",0.84,0.75),
    ("141002","Ludhiana Model Town","Ludhiana","Punjab",30.9020,75.8481,95000,850000,"family","tier1",0.87,0.70),
    ("141003","Ludhiana Dugri","Ludhiana","Punjab",30.8836,75.8614,88000,780000,"family","tier1",0.86,0.65),
    ("141010","Ludhiana BRS Nagar","Ludhiana","Punjab",30.9102,75.8262,78000,900000,"youth","tier1",0.88,0.62),
    # Amritsar
    ("143001","Amritsar City","Amritsar","Punjab",31.6340,74.8723,95000,580000,"working","tier1",0.83,0.75),
    ("143002","Amritsar Lawrence Road","Amritsar","Punjab",31.6450,74.8650,85000,620000,"family","tier1",0.84,0.68),
    ("143006","Golden Temple Area","Amritsar","Punjab",31.6200,74.8765,78000,520000,"working","tier1",0.82,0.80),
    # Faridabad
    ("121001","Faridabad NIT","Faridabad","Haryana",28.4082,77.3178,115000,620000,"working","metro",0.87,0.68),
    ("121002","Faridabad Industrial","Faridabad","Haryana",28.3943,77.3119,100000,580000,"working","metro",0.85,0.65),
    # Rohtak
    ("124001","Rohtak City","Rohtak","Haryana",28.8955,76.6066,88000,520000,"working","tier2",0.82,0.65),
    # Panipat
    ("132001","Panipat","Panipat","Haryana",29.3909,76.9635,75000,500000,"working","tier2",0.81,0.62),
    # Patiala
    ("147001","Patiala","Patiala","Punjab",30.3398,76.3869,78000,580000,"working","tier2",0.84,0.68),
    # Jalandhar
    ("144001","Jalandhar City","Jalandhar","Punjab",31.3260,75.5762,88000,600000,"working","tier2",0.84,0.70),

    # ── ANDHRA PRADESH ────────────────────────────────────────────────
    ("530001","Visakhapatnam City","Visakhapatnam","Andhra Pradesh",17.6868,83.2185,88000,620000,"working","tier1",0.85,0.75),
    ("530002","Dwaraka Nagar","Visakhapatnam","Andhra Pradesh",17.7231,83.3012,78000,750000,"youth","tier1",0.87,0.70),
    ("530003","Seethammadhara","Visakhapatnam","Andhra Pradesh",17.7203,83.3068,72000,820000,"family","tier1",0.88,0.65),
    ("530013","Jagadamba Junction","Visakhapatnam","Andhra Pradesh",17.7042,83.2988,80000,700000,"working","tier1",0.86,0.72),
    ("530022","MVP Colony","Visakhapatnam","Andhra Pradesh",17.7400,83.3200,85000,850000,"family","tier1",0.89,0.68),
    # Vijayawada
    ("520001","Vijayawada City","Krishna","Andhra Pradesh",16.5062,80.6480,88000,580000,"working","tier1",0.84,0.75),
    ("520002","Governorpet","Krishna","Andhra Pradesh",16.5145,80.6326,80000,620000,"working","tier1",0.85,0.72),
    ("520010","Patamata","Krishna","Andhra Pradesh",16.5258,80.6283,75000,680000,"family","tier1",0.85,0.65),
    ("520012","MG Road Vijayawada","Krishna","Andhra Pradesh",16.5078,80.6403,70000,700000,"working","tier1",0.86,0.70),
    # Guntur
    ("522001","Guntur City","Guntur","Andhra Pradesh",16.3067,80.4365,82000,520000,"working","tier2",0.83,0.68),
    ("522002","Brodipeta","Guntur","Andhra Pradesh",16.3100,80.4288,72000,560000,"working","tier2",0.84,0.65),
    # Rajahmundry
    ("533101","Rajahmundry","East Godavari","Andhra Pradesh",17.0005,81.8040,75000,500000,"working","tier2",0.83,0.65),
    # Tirupati
    ("517501","Tirupati","Chittoor","Andhra Pradesh",13.6288,79.4192,78000,480000,"working","tier2",0.82,0.68),

    # ── KERALA ────────────────────────────────────────────────────────
    ("695001","Thiruvananthapuram","Thiruvananthapuram","Kerala",8.5241,76.9366,85000,680000,"working","tier1",0.96,0.72),
    ("695003","Statue Junction","Thiruvananthapuram","Kerala",8.5047,76.9420,78000,720000,"working","tier1",0.96,0.75),
    ("695008","Kowdiar","Thiruvananthapuram","Kerala",8.5235,76.9260,65000,1000000,"family","tier1",0.97,0.65),
    ("695011","Pattom","Thiruvananthapuram","Kerala",8.5329,76.9305,72000,900000,"family","tier1",0.96,0.62),
    ("695034","Kazhakuttam","Thiruvananthapuram","Kerala",8.5649,76.8749,78000,1000000,"youth","tier1",0.95,0.60),
    # Kochi/Ernakulam
    ("682001","Ernakulam","Ernakulam","Kerala",9.9816,76.2999,88000,820000,"working","metro",0.96,0.78),
    ("682002","Fort Kochi","Ernakulam","Kerala",9.9631,76.2428,65000,750000,"working","tier1",0.95,0.72),
    ("682011","Kochi North","Ernakulam","Kerala",9.9923,76.2780,80000,780000,"family","metro",0.96,0.70),
    ("682016","Edapally","Ernakulam","Kerala",10.0284,76.3075,88000,920000,"youth","metro",0.95,0.68),
    ("682021","Kakkanad","Ernakulam","Kerala",10.0119,76.3508,85000,1100000,"youth","metro",0.95,0.62),
    ("682030","Aluva","Ernakulam","Kerala",10.1000,76.3500,72000,750000,"working","tier1",0.95,0.65),
    # Kozhikode
    ("673001","Kozhikode City","Kozhikode","Kerala",11.2588,75.7804,80000,620000,"working","tier1",0.94,0.72),
    ("673004","Chevayur","Kozhikode","Kerala",11.2750,75.8050,68000,580000,"family","tier1",0.93,0.62),
    # Thrissur
    ("680001","Thrissur","Thrissur","Kerala",10.5276,76.2144,78000,620000,"working","tier1",0.95,0.70),
    ("680005","Punkunnam","Thrissur","Kerala",10.5350,76.2100,68000,580000,"family","tier1",0.94,0.65),
    # Kollam
    ("691001","Kollam","Kollam","Kerala",8.8932,76.6141,72000,580000,"working","tier2",0.94,0.65),

    # ── MADHYA PRADESH ────────────────────────────────────────────────
    ("462001","Bhopal City","Bhopal","Madhya Pradesh",23.2599,77.4126,90000,540000,"working","tier1",0.82,0.72),
    ("462003","Habibganj","Bhopal","Madhya Pradesh",23.2323,77.4376,80000,720000,"youth","tier1",0.85,0.68),
    ("462011","Arera Colony","Bhopal","Madhya Pradesh",23.2159,77.4304,75000,800000,"family","tier1",0.86,0.65),
    ("462016","MP Nagar","Bhopal","Madhya Pradesh",23.2310,77.4350,82000,900000,"youth","tier1",0.87,0.72),
    ("462023","Ayodhya Bypass","Bhopal","Madhya Pradesh",23.2650,77.3900,68000,650000,"working","tier1",0.83,0.60),
    ("462043","Bairagarh","Bhopal","Madhya Pradesh",23.2826,77.3541,65000,520000,"family","tier1",0.80,0.55),
    # Indore
    ("452001","Indore City","Indore","Madhya Pradesh",22.7196,75.8577,98000,650000,"working","tier1",0.85,0.75),
    ("452002","Vijay Nagar","Indore","Madhya Pradesh",22.7400,75.8600,88000,780000,"youth","tier1",0.87,0.72),
    ("452010","Rajwada","Indore","Madhya Pradesh",22.7179,75.8550,80000,600000,"working","tier1",0.83,0.75),
    ("452014","Sapna Sangeeta","Indore","Madhya Pradesh",22.7310,75.8720,72000,700000,"family","tier1",0.85,0.68),
    ("452018","Bicholi Mardana","Indore","Madhya Pradesh",22.7640,75.8970,65000,850000,"youth","tier1",0.86,0.62),
    # Gwalior
    ("474001","Gwalior City","Gwalior","Madhya Pradesh",26.2183,78.1828,82000,500000,"working","tier2",0.79,0.68),
    ("474002","Gwalior Lashkar","Gwalior","Madhya Pradesh",26.2124,78.1761,72000,480000,"family","tier2",0.78,0.65),
    # Jabalpur
    ("482001","Jabalpur City","Jabalpur","Madhya Pradesh",23.1815,79.9864,85000,490000,"working","tier2",0.80,0.68),
    ("482002","Napier Town","Jabalpur","Madhya Pradesh",23.1640,79.9461,75000,520000,"working","tier2",0.81,0.65),
    # Ujjain
    ("456001","Ujjain","Ujjain","Madhya Pradesh",23.1793,75.7849,72000,460000,"working","tier2",0.78,0.65),

    # ── BIHAR ─────────────────────────────────────────────────────────
    ("800001","Patna City","Patna","Bihar",25.5941,85.1376,95000,480000,"working","tier1",0.77,0.75),
    ("800002","Patna Boring Road","Patna","Bihar",25.6090,85.0972,85000,600000,"youth","tier1",0.81,0.70),
    ("800007","Kankarbagh","Patna","Bihar",25.5942,85.1376,90000,520000,"family","tier1",0.78,0.68),
    ("800013","Bailey Road","Patna","Bihar",25.6123,85.1000,80000,680000,"youth","tier1",0.82,0.65),
    ("800020","Danapur","Patna","Bihar",25.6143,85.0454,75000,480000,"working","tier1",0.77,0.60),
    ("800027","Patliputra","Patna","Bihar",25.6169,85.0590,72000,650000,"youth","tier1",0.83,0.62),
    # Gaya
    ("823001","Gaya City","Gaya","Bihar",24.7955,85.0002,72000,420000,"working","tier2",0.72,0.62),
    ("823002","Bodh Gaya","Gaya","Bihar",24.6961,84.9914,45000,400000,"working","tier3",0.70,0.60),
    # Muzaffarpur
    ("842001","Muzaffarpur","Muzaffarpur","Bihar",26.1209,85.3647,78000,410000,"working","tier2",0.73,0.60),
    # Bhagalpur
    ("812001","Bhagalpur","Bhagalpur","Bihar",25.2425,86.9842,68000,400000,"working","tier2",0.72,0.58),

    # ── ODISHA ────────────────────────────────────────────────────────
    ("751001","Bhubaneswar City","Khurda","Odisha",20.2961,85.8245,85000,580000,"working","tier1",0.87,0.72),
    ("751006","Saheed Nagar","Khurda","Odisha",20.2880,85.8500,75000,680000,"youth","tier1",0.88,0.68),
    ("751009","Rajmahal","Khurda","Odisha",20.2651,85.8414,68000,720000,"working","tier1",0.88,0.65),
    ("751015","IRC Village","Khurda","Odisha",20.2960,85.8076,72000,800000,"youth","tier1",0.89,0.62),
    ("751030","Patia","Khurda","Odisha",20.3503,85.8245,80000,900000,"youth","tier1",0.90,0.60),
    # Cuttack
    ("753001","Cuttack City","Cuttack","Odisha",20.4625,85.8830,82000,500000,"working","tier2",0.85,0.68),
    ("753003","Badambadi","Cuttack","Odisha",20.4830,85.8750,72000,480000,"working","tier2",0.83,0.65),
    # Rourkela
    ("769001","Rourkela","Sundargarh","Odisha",22.2604,84.8536,78000,520000,"working","tier2",0.85,0.62),

    # ── ASSAM ─────────────────────────────────────────────────────────
    ("781001","Guwahati City","Kamrup","Assam",26.1445,91.7362,88000,520000,"working","tier1",0.85,0.72),
    ("781003","Paltan Bazar","Kamrup","Assam",26.1859,91.7447,78000,480000,"working","tier1",0.84,0.75),
    ("781005","Fancy Bazar","Kamrup","Assam",26.1884,91.7447,72000,450000,"working","tier1",0.83,0.72),
    ("781007","Dispur","Kamrup","Assam",26.1355,91.7867,65000,650000,"youth","tier1",0.87,0.68),
    ("781022","Beltola","Kamrup","Assam",26.1072,91.7638,70000,580000,"family","tier1",0.85,0.62),
    # Silchar
    ("788001","Silchar","Cachar","Assam",24.8333,92.7789,65000,430000,"working","tier2",0.81,0.62),
    # Dibrugarh
    ("786001","Dibrugarh","Dibrugarh","Assam",27.4728,94.9120,58000,420000,"working","tier2",0.80,0.60),

    # ── JHARKHAND ─────────────────────────────────────────────────────
    ("834001","Ranchi City","Ranchi","Jharkhand",23.3441,85.3096,85000,520000,"working","tier2",0.80,0.68),
    ("834002","Doranda","Ranchi","Jharkhand",23.3521,85.3219,75000,580000,"youth","tier2",0.82,0.62),
    ("834003","Lalpur","Ranchi","Jharkhand",23.3568,85.3432,68000,620000,"working","tier2",0.83,0.65),
    # Jamshedpur
    ("831001","Jamshedpur Bistupur","East Singhbhum","Jharkhand",22.8046,86.2029,88000,680000,"working","tier2",0.84,0.72),
    ("831002","Sakchi","East Singhbhum","Jharkhand",22.7994,86.1905,80000,620000,"working","tier2",0.83,0.68),
    # Dhanbad
    ("826001","Dhanbad","Dhanbad","Jharkhand",23.7957,86.4304,82000,520000,"working","tier2",0.80,0.65),
    # Bokaro
    ("827001","Bokaro","Bokaro","Jharkhand",23.6693,86.1511,72000,580000,"working","tier2",0.81,0.60),

    # ── CHHATTISGARH ─────────────────────────────────────────────────
    ("492001","Raipur City","Raipur","Chhattisgarh",21.2514,81.6296,88000,520000,"working","tier2",0.81,0.70),
    ("492010","Shankar Nagar","Raipur","Chhattisgarh",21.2636,81.6312,78000,620000,"youth","tier2",0.83,0.65),
    ("492015","Pandri","Raipur","Chhattisgarh",21.2440,81.6410,72000,580000,"family","tier2",0.82,0.60),
    # Bhilai
    ("490001","Bhilai","Durg","Chhattisgarh",21.2090,81.3628,85000,560000,"working","tier2",0.82,0.65),
    # Bilaspur
    ("495001","Bilaspur","Bilaspur","Chhattisgarh",22.0796,82.1391,72000,480000,"working","tier2",0.79,0.60),

    # ── UTTARAKHAND ──────────────────────────────────────────────────
    ("248001","Dehradun City","Dehradun","Uttarakhand",30.3165,78.0322,88000,600000,"youth","tier2",0.86,0.72),
    ("248002","Rajpur Road","Dehradun","Uttarakhand",30.3474,78.0485,78000,750000,"youth","tier2",0.87,0.68),
    ("248003","Patel Nagar Dehradun","Dehradun","Uttarakhand",30.2999,78.0536,72000,580000,"family","tier2",0.85,0.62),
    # Haridwar
    ("249401","Haridwar","Haridwar","Uttarakhand",29.9457,78.1642,75000,450000,"working","tier2",0.82,0.68),
    # Rishikesh
    ("249201","Rishikesh","Dehradun","Uttarakhand",30.0869,78.2676,58000,420000,"youth","tier2",0.84,0.65),
    # Nainital
    ("263001","Nainital","Nainital","Uttarakhand",29.3803,79.4636,35000,480000,"working","tier3",0.85,0.62),
    # Roorkee
    ("247667","Roorkee","Haridwar","Uttarakhand",29.8543,77.8880,55000,500000,"youth","tier2",0.84,0.62),

    # ── HIMACHAL PRADESH ─────────────────────────────────────────────
    ("171001","Shimla City","Shimla","Himachal Pradesh",31.1048,77.1734,38000,550000,"working","tier2",0.90,0.68),
    ("171002","Shimla Mall Road","Shimla","Himachal Pradesh",31.1063,77.1722,32000,620000,"working","tier2",0.91,0.72),
    ("175131","Manali","Kullu","Himachal Pradesh",32.2432,77.1892,25000,500000,"youth","tier3",0.88,0.70),
    ("176001","Dharamsala","Kangra","Himachal Pradesh",32.2190,76.3234,28000,480000,"youth","tier3",0.89,0.65),
    # Solan
    ("173212","Solan","Solan","Himachal Pradesh",30.9045,77.0967,32000,500000,"working","tier3",0.87,0.58),

    # ── GOA ──────────────────────────────────────────────────────────
    ("403001","Panaji","North Goa","Goa",15.4909,73.8278,40000,850000,"working","tier2",0.91,0.75),
    ("403004","Mapusa","North Goa","Goa",15.5938,73.8100,35000,700000,"working","tier2",0.89,0.68),
    ("403601","Margao","South Goa","Goa",15.2832,73.9862,38000,720000,"working","tier2",0.90,0.70),
    ("403006","Calangute","North Goa","Goa",15.5440,73.7552,22000,780000,"youth","tier2",0.88,0.72),
    ("403518","Vasco da Gama","South Goa","Goa",15.3986,73.8154,40000,680000,"working","tier2",0.88,0.65),

    # ── JAMMU & KASHMIR ──────────────────────────────────────────────
    ("180001","Jammu City","Jammu","Jammu and Kashmir",32.7266,74.8570,88000,500000,"working","tier2",0.82,0.70),
    ("180002","Gandhi Nagar Jammu","Jammu","Jammu and Kashmir",32.7380,74.8720,78000,580000,"youth","tier2",0.84,0.65),
    ("190001","Srinagar City","Srinagar","Jammu and Kashmir",34.0837,74.7973,88000,520000,"working","tier2",0.79,0.68),
    ("190003","Lal Chowk","Srinagar","Jammu and Kashmir",34.0837,74.7973,72000,500000,"working","tier2",0.80,0.72),
    # Udhampur
    ("182101","Udhampur","Udhampur","Jammu and Kashmir",32.9260,75.1416,45000,400000,"working","tier3",0.78,0.55),

    # ── TRIPURA ──────────────────────────────────────────────────────
    ("799001","Agartala City","West Tripura","Tripura",23.8315,91.2868,62000,440000,"working","tier2",0.88,0.65),
    ("799002","Agartala Krishnanagar","West Tripura","Tripura",23.8439,91.2870,52000,420000,"family","tier2",0.87,0.58),

    # ── MEGHALAYA ────────────────────────────────────────────────────
    ("793001","Shillong City","East Khasi Hills","Meghalaya",25.5788,91.8933,58000,520000,"youth","tier2",0.89,0.68),
    ("793002","Shillong Police Bazar","East Khasi Hills","Meghalaya",25.5706,91.8836,48000,580000,"working","tier2",0.90,0.72),

    # ── MANIPUR ──────────────────────────────────────────────────────
    ("795001","Imphal City","Imphal West","Manipur",24.8170,93.9368,62000,420000,"working","tier2",0.88,0.65),

    # ── NAGALAND ─────────────────────────────────────────────────────
    ("797001","Kohima","Kohima","Nagaland",25.6586,94.1086,38000,450000,"working","tier2",0.87,0.60),

    # ── MIZORAM ──────────────────────────────────────────────────────
    ("796001","Aizawl City","Aizawl","Mizoram",23.7271,92.7176,42000,450000,"working","tier2",0.92,0.62),

    # ── SIKKIM ───────────────────────────────────────────────────────
    ("737101","Gangtok","East Sikkim","Sikkim",27.3389,88.6065,25000,520000,"youth","tier3",0.89,0.65),

    # ── ARUNACHAL PRADESH ────────────────────────────────────────────
    ("791111","Itanagar","Papum Pare","Arunachal Pradesh",27.0844,93.6053,35000,450000,"working","tier3",0.83,0.58),

    # ── ANDAMAN & NICOBAR ────────────────────────────────────────────
    ("744101","Port Blair","South Andaman","Andaman and Nicobar",11.6234,92.7265,32000,620000,"working","tier2",0.86,0.68),

    # ── LAKSHADWEEP ──────────────────────────────────────────────────
    ("682555","Kavaratti","Lakshadweep","Lakshadweep",10.5669,72.6420,8000,480000,"working","tier3",0.93,0.50),

    # ── PUDUCHERRY ───────────────────────────────────────────────────
    ("605001","Pondicherry","Puducherry","Puducherry",11.9416,79.8083,65000,600000,"working","tier2",0.88,0.72),
    ("605005","Puducherry Beach","Puducherry","Puducherry",11.9255,79.8304,55000,650000,"youth","tier2",0.89,0.70),

    # ── TELANGANA EXTRA ───────────────────────────────────────────────
    ("500097","Kokapet","Hyderabad","Telangana",17.4067,78.3244,65000,1400000,"youth","metro",0.93,0.55),
    ("500098","Nanakramguda","Hyderabad","Telangana",17.4133,78.3400,60000,1600000,"youth","metro",0.94,0.58),
    ("501301","Shamshabad","Hyderabad","Telangana",17.2544,78.3881,45000,550000,"working","tier2",0.80,0.50),
    # Warangal extra
    ("506370","Narsampet","Warangal","Telangana",17.9272,79.8963,35000,360000,"working","tier3",0.74,0.45),

    # ── KARNATAKA EXTRA ───────────────────────────────────────────────
    ("560099","Devanahalli","Bangalore Rural","Karnataka",13.2460,77.7115,38000,550000,"working","tier2",0.83,0.48),
    ("572101","Tumkur","Tumakuru","Karnataka",13.3379,77.1173,75000,480000,"working","tier2",0.83,0.62),
    ("573201","Hassan","Hassan","Karnataka",13.0033,76.0994,60000,440000,"working","tier2",0.82,0.60),
    ("576101","Udupi","Udupi","Karnataka",13.3409,74.7421,55000,500000,"working","tier2",0.87,0.62),
    ("585101","Gulbarga","Kalaburagi","Karnataka",17.3297,76.8343,82000,420000,"working","tier2",0.74,0.60),

    # ── MAHARASHTRA EXTRA ────────────────────────────────────────────
    ("400706","Navi Mumbai Vashi","Thane","Maharashtra",19.0748,73.0161,95000,950000,"working","metro",0.92,0.68),
    ("400701","Navi Mumbai Nerul","Thane","Maharashtra",19.0368,73.0170,88000,900000,"family","metro",0.91,0.65),
    ("421001","Kalyan","Thane","Maharashtra",19.2403,73.1305,128000,620000,"family","metro",0.88,0.65),
    ("401501","Vasai","Palghar","Maharashtra",19.3919,72.8397,85000,580000,"working","tier1",0.86,0.60),
    ("413003","Solapur East","Solapur","Maharashtra",17.6750,75.9200,78000,460000,"working","tier2",0.79,0.55),
    ("416416","Kolhapur South","Kolhapur","Maharashtra",16.6910,74.2290,68000,520000,"family","tier2",0.83,0.58),

    # ── RAJASTHAN EXTRA ──────────────────────────────────────────────
    ("324010","Kota Industrial","Kota","Rajasthan",25.1840,75.8700,60000,520000,"working","tier2",0.80,0.58),
    ("305003","Ajmer Nasirabad","Ajmer","Rajasthan",26.3120,74.7240,52000,400000,"working","tier2",0.76,0.52),
    ("313004","Udaipur Hiran Magri","Udaipur","Rajasthan",24.5980,73.7000,58000,550000,"youth","tier2",0.82,0.58),
    ("334001","Bikaner","Bikaner","Rajasthan",28.0229,73.3119,80000,450000,"working","tier2",0.76,0.65),
    ("313001","Udaipur City","Udaipur","Rajasthan",24.5854,73.7125,72000,520000,"working","tier2",0.81,0.68),

    # ── GUJARAT EXTRA ────────────────────────────────────────────────
    ("380028","Ahmedabad Gota","Ahmedabad","Gujarat",23.0920,72.5290,78000,850000,"youth","metro",0.89,0.60),
    ("380061","Ahmedabad Prahlad Nagar","Ahmedabad","Gujarat",23.0175,72.5018,82000,1400000,"youth","metro",0.92,0.68),
    ("361001","Jamnagar","Jamnagar","Gujarat",22.4707,70.0577,75000,520000,"working","tier2",0.83,0.65),
    ("364001","Bhavnagar","Bhavnagar","Gujarat",21.7645,72.1519,78000,500000,"working","tier2",0.82,0.62),
    ("396001","Valsad","Valsad","Gujarat",20.5992,72.9342,55000,560000,"working","tier2",0.84,0.60),
    ("394601","Ankleshwar","Bharuch","Gujarat",21.6268,92.8610,62000,620000,"working","tier2",0.82,0.58),

    # ── TAMIL NADU EXTRA ─────────────────────────────────────────────
    ("641046","Coimbatore GN Mills","Coimbatore","Tamil Nadu",11.0380,77.0180,70000,680000,"working","tier1",0.87,0.58),
    ("625020","Madurai Palanganatham","Madurai","Tamil Nadu",9.8980,78.1310,65000,500000,"family","tier1",0.82,0.58),
    ("620008","Trichy Cantonment","Tiruchirappalli","Tamil Nadu",10.7768,78.7066,62000,560000,"working","tier1",0.87,0.62),
    ("636007","Salem Suramangalam","Salem","Tamil Nadu",11.6800,78.1900,75000,500000,"family","tier2",0.84,0.60),
    ("627002","Tirunelveli Palayamkottai","Tirunelveli","Tamil Nadu",8.7216,77.7382,68000,470000,"working","tier2",0.85,0.62),
    ("641601","Tiruppur","Tiruppur","Tamil Nadu",11.1075,77.3398,95000,650000,"working","tier1",0.84,0.72),
    ("623001","Ramanathapuram","Ramanathapuram","Tamil Nadu",9.3714,78.8306,52000,400000,"working","tier3",0.78,0.55),

    # ── UP EXTRA ─────────────────────────────────────────────────────
    ("244001","Moradabad","Moradabad","Uttar Pradesh",28.8386,78.7733,95000,500000,"working","tier2",0.77,0.65),
    ("243001","Bareilly","Bareilly","Uttar Pradesh",28.3670,79.4304,108000,490000,"working","tier2",0.76,0.68),
    ("221010","Sarnath","Varanasi","Uttar Pradesh",25.3741,83.0218,35000,420000,"working","tier2",0.79,0.58),
    ("273001","Gorakhpur","Gorakhpur","Uttar Pradesh",26.7606,83.3732,95000,470000,"working","tier2",0.76,0.65),
    ("302033","Jaipur Jagatpura Ext","Jaipur","Rajasthan",26.7900,75.8600,62000,560000,"youth","tier2",0.81,0.55),

    # ── KERALA EXTRA ─────────────────────────────────────────────────
    ("682032","Aluva Perumbavoor","Ernakulam","Kerala",10.1070,76.4050,55000,650000,"working","tier1",0.94,0.58),
    ("695043","Thiruvananthapuram Technopark","Thiruvananthapuram","Kerala",8.5570,76.8787,62000,1100000,"youth","tier1",0.95,0.55),
    ("673020","Kozhikode Beypore","Kozhikode","Kerala",11.1737,75.8006,48000,520000,"working","tier2",0.92,0.55),
    ("680002","Thrissur Swaraj Round","Thrissur","Kerala",10.5180,76.2106,65000,680000,"working","tier1",0.95,0.70),
    ("691002","Kollam Kadappakada","Kollam","Kerala",8.8862,76.6141,62000,550000,"family","tier2",0.93,0.62),

    # ── BIHAR EXTRA ──────────────────────────────────────────────────
    ("800001","Patna GPO","Patna","Bihar",25.6127,85.1536,88000,500000,"working","tier1",0.78,0.72),
    ("843101","Sitamarhi","Sitamarhi","Bihar",26.5900,85.4900,48000,350000,"working","tier3",0.65,0.48),
    ("845401","Motihari","East Champaran","Bihar",26.6494,84.9125,52000,360000,"working","tier3",0.66,0.50),

    # ── ODISHA EXTRA ─────────────────────────────────────────────────
    ("769015","Rourkela Industrial","Sundargarh","Odisha",22.2400,84.8650,65000,560000,"working","tier2",0.84,0.58),
    ("760001","Berhampur","Ganjam","Odisha",19.3149,84.7941,72000,460000,"working","tier2",0.82,0.62),
    ("768001","Sambalpur","Sambalpur","Odisha",21.4669,83.9812,65000,450000,"working","tier2",0.81,0.58),

    # ── MP EXTRA ─────────────────────────────────────────────────────
    ("482004","Jabalpur Madan Mahal","Jabalpur","Madhya Pradesh",23.1750,79.9760,65000,500000,"family","tier2",0.80,0.60),
    ("474012","Gwalior Morar","Gwalior","Madhya Pradesh",26.2390,78.2200,62000,460000,"working","tier2",0.78,0.58),
    ("485001","Satna","Satna","Madhya Pradesh",24.5668,80.8322,65000,430000,"working","tier2",0.77,0.55),

    # ── PUNE EXTRA ───────────────────────────────────────────────────
    ("411021","Hadapsar Industrial","Pune","Maharashtra",18.4820,73.9410,120000,680000,"working","metro",0.88,0.70),
    ("412101","Nanded City Pune","Pune","Maharashtra",18.4640,73.8058,80000,1100000,"youth","metro",0.92,0.60),
    ("412307","Pimpri-Chinchwad","Pune","Maharashtra",18.6279,73.8001,145000,750000,"working","metro",0.88,0.68),
    ("411027","Kharadi","Pune","Maharashtra",18.5517,73.9411,82000,1200000,"youth","metro",0.93,0.62),

    # ── WEST BENGAL EXTRA ────────────────────────────────────────────
    ("711102","Howrah Golabari","Howrah","West Bengal",22.5880,88.2980,88000,480000,"working","metro",0.83,0.68),
    ("741101","Krishnanagar","Nadia","West Bengal",23.4024,88.4989,62000,430000,"working","tier2",0.80,0.60),
    ("742101","Berhampore","Murshidabad","West Bengal",24.1040,88.2450,65000,400000,"working","tier2",0.79,0.58),
    ("700110","Barrackpore","North 24 Parganas","West Bengal",22.7639,88.3640,80000,520000,"working","metro",0.85,0.62),

    # ── HARYANA EXTRA ────────────────────────────────────────────────
    ("121001","Faridabad Ballabgarh","Faridabad","Haryana",28.3436,77.3219,92000,580000,"working","metro",0.86,0.62),
    ("135001","Yamunanagar","Yamuna Nagar","Haryana",30.1290,77.2674,72000,500000,"working","tier2",0.82,0.62),
    ("132103","Karnal","Karnal","Haryana",29.6857,76.9905,80000,520000,"working","tier2",0.82,0.65),
    ("125001","Hisar","Hisar","Haryana",29.1492,75.7217,82000,480000,"working","tier2",0.79,0.62),

    # ── NORTHEAST EXTRA ──────────────────────────────────────────────
    ("781101","Guwahati Pragjyotishpur","Kamrup","Assam",26.1750,91.8250,58000,480000,"youth","tier2",0.84,0.58),
    ("781040","Guwahati Maligaon","Kamrup","Assam",26.1630,91.7050,65000,500000,"working","tier1",0.85,0.62),
    ("794001","Tura","South Garo Hills","Meghalaya",25.5148,90.2134,28000,390000,"working","tier3",0.80,0.50),
    ("796007","Lunglei","Lunglei","Mizoram",22.8808,92.7349,18000,380000,"working","tier3",0.90,0.45),
]


# ────────────────────────────────────────────────────────────────────
# Build the indexed dictionary
# ────────────────────────────────────────────────────────────────────
PINCODE_DB: dict[str, PincodeEntry] = {}
for row in _RAW:
    pin, city, district, state, lat, lng, pop, income, age, tier, lit, density = row
    if pin not in PINCODE_DB:          # skip exact duplicates
        PINCODE_DB[pin] = PincodeEntry(
            city=city, district=district, state=state,
            lat=lat, lng=lng,
            population=pop, avg_income=income,
            age_dominant=age, tier=tier,
            literacy_rate=lit,
            commercial_density=density,
        )


# ── Helpers ─────────────────────────────────────────────────────────
def get(pincode: str) -> PincodeEntry | None:
    return PINCODE_DB.get(pincode)

def search_by_city(city_query: str, limit: int = 10) -> list[dict]:
    q = city_query.lower()
    results = []
    for pin, entry in PINCODE_DB.items():
        if q in entry["city"].lower() or q in entry["district"].lower():
            results.append({"pincode": pin, **entry})
            if len(results) >= limit:
                break
    return results

def get_by_state(state: str) -> list[dict]:
    return [{"pincode": pin, **entry} for pin, entry in PINCODE_DB.items()
            if entry["state"].lower() == state.lower()]

def get_all_states() -> list[str]:
    return sorted(set(e["state"] for e in PINCODE_DB.values()))

def get_cities_by_state() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for entry in PINCODE_DB.values():
        result.setdefault(entry["state"], [])
        if entry["city"] not in result[entry["state"]]:
            result[entry["state"]].append(entry["city"])
    return {state: sorted(cities) for state, cities in sorted(result.items())}

def suggest(query: str, limit: int = 8) -> list[dict]:
    q = query.lower().strip()
    if not q:
        return []
    results = []
    for pin, entry in PINCODE_DB.items():
        score = 0
        if pin.startswith(q):
            score = 3
        elif q in entry["city"].lower():
            score = 2
        elif q in entry["district"].lower() or q in entry["state"].lower():
            score = 1
        if score:
            results.append((score, pin, entry))
    results.sort(key=lambda x: -x[0])
    return [{"pincode": p, **e, "_score": s} for s, p, e in results[:limit]]

TOTAL_PINCODES = len(PINCODE_DB)
ALL_STATES = get_all_states()
