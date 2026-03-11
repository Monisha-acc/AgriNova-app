# Government Schemes Database for Tamil Nadu Farmers

# Central Government Schemes
CENTRAL_SCHEMES = [
    {
        "id": "pm_kisan",
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "name_ta": "பிரதமர் கிசான் சம்மன் நிதி (PM-KISAN)",
        "description": "Income support to farmers",
        "description_ta": "விவசாயிகளுக்கு வருமான ஆதரவு",
        "benefits": "₹6000/year in 3 installments",
        "benefits_ta": "ஆண்டுக்கு ₹6000 (3 தவணைகளில்)",
        "eligibility": ["All landholding farmers"],
        "type": "Income Support",
        "type_ta": "வருமான ஆதரவு",
        "link": "https://pmkisan.gov.in/",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "soil_health",
        "name": "Soil Health Card Scheme",
        "name_ta": "மண் ஆரோக்கிய அட்டை திட்டம்",
        "description": "Free soil health cards for fertiliser recommendations",
        "description_ta": "உரப் பரிந்துரைகளுக்கான இலவச மண் ஆரோக்கிய அட்டைகள்",
        "benefits": "Soil health status and nutrient recommendations",
        "benefits_ta": "மண் வள நிலை மற்றும் ஊட்டச்சத்து பரிந்துரைகள்",
        "eligibility": ["All farmers"],
        "type": "Advisory",
        "type_ta": "ஆலோசனை",
        "link": "https://soilhealth.dac.gov.in/",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "pmfby",
        "name": "PM Fasal Bima Yojana (Crop Insurance)",
        "name_ta": "பிரதமர் பயிர் காப்பீட்டு திட்டம் (PMFBY)",
        "description": "Insurance against crop loss",
        "description_ta": "பயிர் இழப்பிற்கு எதிரான காப்பீடு",
        "benefits": "Financial support in case of crop failure",
        "benefits_ta": "பயிர் பாதிப்பு ஏற்படும் போது நிதி உதவி",
        "eligibility": ["Farmers with insurable crops"],
        "type": "Insurance",
        "type_ta": "காப்பீடு",
        "link": "https://pmfby.gov.in/",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "kcc",
        "name": "Kisan Credit Card (KCC)",
        "name_ta": "கிசான் கடன் அட்டை (KCC)",
        "description": "Low-interest credit for cultivation & allied activities",
        "description_ta": "விவசாயம் மற்றும் அதனைச் சார்ந்த தொழில்களுக்கு குறைந்த வட்டி கடன்",
        "benefits": "Credit at 4% interest rate (with prompt repayment)",
        "benefits_ta": "4% வட்டியில் கடன் (சரியான நேரத்தில் திரும்ப செலுத்தினால்)",
        "eligibility": ["All farmers-individuals/joint borrowers"],
        "type": "Credit",
        "type_ta": "கடன்",
        "link": "https://www.myscheme.gov.in/schemes/kcc",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "enam",
        "name": "National Agriculture Market (e-NAM)",
        "name_ta": "தேசிய வேளான் சந்தை (e-NAM)",
        "description": "Online mandi market for better pricing",
        "description_ta": "சிறந்த விலைக்கு ஆன்லைன் மண்டி சந்தை",
        "benefits": "Transparent auction process, better price realization",
        "benefits_ta": "வெளிப்படையான ஏலம், அதிக லாபம்",
        "eligibility": ["Farmers registered with APMC"],
        "type": "Market Linkage",
        "type_ta": "சந்தை இணைப்பு",
        "link": "https://enam.gov.in/web/",
        "adoption_level": ["Moderate", "High"]
    },
    {
        "id": "pmksy",
        "name": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)",
        "name_ta": "பிரதமர் கிரிஷி சின்சாயி யோஜனா (PMKSY)",
        "description": "Micro-irrigation and watershed development",
        "description_ta": "நுண்ணீர் பாசனம் மற்றும் நீர்முனை மேம்பாடு",
        "benefits": "Subsidy for drip and sprinkler irrigation systems",
        "benefits_ta": "சொட்டு மற்றும் தெளிப்பு நீர் பாசனத்திற்கு மானியம்",
        "eligibility": ["Farmers with land and water source"],
        "type": "Irrigation Subsidy",
        "type_ta": "பாசன மானியம்",
        "link": "https://pmksy.gov.in/",
        "adoption_level": ["Moderate", "High"]
    },
    {
        "id": "pm_kusum",
        "name": "PM-KUSUM (Solar Pumps)",
        "name_ta": "பிஎம்-குசும் (சூரிய சக்தி பம்புகள்)",
        "description": "Subsidy for solar pumps and renewable energy",
        "description_ta": "சூரிய சக்தி பம்புகளுக்கான மானியம்",
        "benefits": "Subsidy up to 60% for standalone solar pumps",
        "benefits_ta": "சூரிய சக்தி பம்புகளுக்கு 60% வரை மானியம்",
        "eligibility": ["Farmers, Panchayats, Cooperatives"],
        "type": "Energy",
        "type_ta": "ஆற்றல்",
        "link": "https://pmkusum.mnre.gov.in/",
        "adoption_level": ["Moderate", "High"]
    },
    {
        "id": "aif",
        "name": "Agriculture Infrastructure Fund (AIF)",
        "name_ta": "வேளாண் உள்கட்டமைப்பு நிதி (AIF)",
        "description": "Loans for post-harvest and value chain infrastructure",
        "description_ta": "அறுவடைக்குப் பின் கட்டமைப்பு உருவாக்க கடன்கள்",
        "benefits": "Interest subvention of 3% per annum up to ₹2 crore",
        "benefits_ta": "₹2 கோடி வரை ஆண்டுக்கு 3% வட்டி மானியம்",
        "eligibility": ["Farmers, FPOs, PACS, Startups"],
        "type": "Infrastructure",
        "type_ta": "உள்கட்டமைப்பு",
        "link": "https://agriinfra.dac.gov.in/",
        "adoption_level": ["High"]
    },
    {
        "id": "svamitva",
        "name": "SVAMITVA Scheme",
        "name_ta": "ஸ்வாமித்வா திட்டம்",
        "description": "Property cards for rural households",
        "description_ta": "கிராமப்புற வீடுகளுக்கான சொத்து அட்டைகள்",
        "benefits": "Record of Rights to village household owners",
        "benefits_ta": "கிராம வீட்டு உரிமையாளர்களுக்கு சொத்து உரிமை ஆவணம்",
        "eligibility": ["Rural homeowners"],
        "type": "Governance",
        "type_ta": "ஆளுமை",
        "link": "https://svamitva.nic.in/",
        "adoption_level": ["Low", "Moderate"]
    }
]

# Tamil Nadu Government Schemes
TAMIL_NADU_SCHEMES = [
    {
        "id": "tn_micro_irrigation",
        "name": "TN Micro Irrigation Subsidy",
        "name_ta": "நுண்ணீர் பாசன மானியத் திட்டம்",
        "description": "Micro Irrigation scheme for state farmers",
        "description_ta": "மாநில விவசாயிகளுக்கான நுண்ணீர் பாசன திட்டம்",
        "benefits": "100% subsidy for small/marginal farmers, 75% for others",
        "benefits_ta": "சிறு/குறு விவசாயிகளுக்கு 100% மானியம், மற்றவர்களுக்கு 75%",
        "eligibility": ["Small/Marginal Farmers: 100%", "Other Farmers: 75%"],
        "type": "Irrigation Subsidy",
        "type_ta": "பாசன மானியம்",
        "link": "https://tnhorticulture.tn.gov.in/horti/pminfo",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "tn_farm_mechanization",
        "name": "Agricultural Mechanization Programme",
        "name_ta": "வேளாண் இயந்திரமயமாக்கல் திட்டம்",
        "description": "Subsidy for purchasing farm machinery",
        "description_ta": "வேளாண் இயந்திரங்கள் வாங்க மானியம்",
        "benefits": "Subsidy for tractors, tillers, harvesters",
        "benefits_ta": "டிராக்டர், உழவு இயந்திரம் வாங்க மானியம்",
        "eligibility": ["All Farmers"],
        "type": "Machinery",
        "type_ta": "இயந்திரங்கள்",
        "link": "https://aed.tn.gov.in/en/agricultural-mechanisation/",
        "adoption_level": ["Moderate", "High"]
    },
    {
        "id": "kalaignar_scheme",
        "name": "Kalaignar Integrated Agriculture Dev. Prog.",
        "name_ta": "கலைஞரின் ஒருங்கிணைந்த வேளாண் வளர்ச்சித் திட்டம்",
        "description": "Integrated development of villages",
        "description_ta": "கிராமங்களின் ஒருங்கிணைந்த வளர்ச்சி",
        "benefits": "Coconut saplings, horticultural plants, farm kits",
        "benefits_ta": "தென்னங்கன்று, தோட்டக்கலை செடிகள் விநியோகம்",
        "eligibility": ["Village residents"],
        "type": "Integrated Dev",
        "type_ta": "ஒருங்கிணைந்த வளம்",
        "link": "https://www.tnagrisnet.tn.gov.in/",
        "adoption_level": ["Low", "Moderate"]
    },
    {
        "id": "tn_free_electricity",
        "name": "Free Electricity for Farmers",
        "name_ta": "விவசாயிகளுக்கு இலவச மின்சாரம்",
        "description": "Free power supply for irrigation pumps",
        "description_ta": "நீர்ப்பாசன பம்புகளுக்கு இலவச மின்சாரம்",
        "benefits": "100% free electricity",
        "benefits_ta": "100% இலவச மின்சாரம்",
        "eligibility": ["Farmers with motor pumpsets"],
        "type": "Energy",
        "type_ta": "ஆற்றல்",
        "link": "https://www.tangedco.gov.in/linkpdf/Agri%20Tariff.pdf",
        "adoption_level": ["Low", "Moderate", "High"]
    },
     {
        "id": "uzhavan_app",
        "name": "Uzhavan App",
        "name_ta": "உழவன் செயலி",
        "description": "One-stop mobile app for all TN agri services",
        "description_ta": "அனைத்து தமிழக வேளாண் சேவைகளுக்கும் ஒரே செயலி",
        "benefits": "Access to 9+ departments services",
        "benefits_ta": "9க்கும் மேற்பட்ட துறை சேவைகளுக்கான அணுகல்",
        "eligibility": ["All Farmers"],
        "type": "Digital Service",
        "type_ta": "டிஜிட்டல் சேவை",
        "link": "https://tnagrisnet.tn.gov.in/",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "tn_soil_health",
        "name": "TN Soil Health Management",
        "name_ta": "தமிழ்நாடு மண் வள மேம்பாடு",
        "description": "Distribution of green manure seeds and bio-fertilizers",
        "description_ta": "பசுந்தாள் உர விதைகள் விநியோகம்",
        "benefits": "Subsidized inputs for soil fertility",
        "benefits_ta": "மண் வளத்திற்கான மானிய உள்ளீடுகள்",
        "eligibility": ["All farmers"],
        "type": "Soil Health",
        "type_ta": "மண் ஆரோக்கியம்",
        "link": "https://tnagrisnet.tn.gov.in/",
        "adoption_level": ["Low", "Moderate"]
    },
    {
        "id": "tn_kudimaramathu",
        "name": "Kudimaramathu (Water Conservation)",
        "name_ta": "குடிமராமத்து (நீர் பாதுகாப்பு)",
        "description": "Tank/irrigation infrastructure restoration",
        "description_ta": "குளம்/நீர்ப்பாசன மறுசீரமைப்பு",
        "benefits": "Improved water storage and availability",
        "benefits_ta": "மேம்படுத்தப்பட்ட நீர் சேமிப்பு மற்றும் கிடைக்கும் தன்மை",
        "eligibility": ["Community participation"],
        "type": "Water Conservation",
        "type_ta": "நீர் பாதுகாப்பு",
        "link": "https://www.tndipr.gov.in/DIPR/en/kudimaramathu/",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "tn_training",
        "name": "Farmers Training / Extension Services",
        "name_ta": "விவசாயிகள் பயிற்சி / விரிவாக்க சேவைகள்",
        "description": "Training and advice at farmer service centres",
        "description_ta": "விவசாயிகள் சேவை மையங்களில் பயிற்சி",
        "benefits": "Knowledge on modern farming techniques",
        "benefits_ta": "நவீன விவசாய நுட்பங்கள் பற்றிய அறிவு",
        "eligibility": ["All farmers"],
        "type": "Training",
        "type_ta": "பயிற்சி",
        "link": "https://www.tnau.ac.in/",
        "adoption_level": ["Low", "Moderate"]
    }
]

# Women & Gender-Inclusive Support
WOMEN_SCHEMES = [
    {
        "id": "women_shg",
        "name": "DAY-NRLM (Support via SHGs)",
        "name_ta": "DAY-NRLM (சுயஉதவி குழுக்கள் ஆதரவு)",
        "description": "Loans, training, and enterprise support for women",
        "description_ta": "பெண்களுக்கான கடன்கள் மற்றும் நிறுவன ஆதரவு",
        "benefits": "Collateral-free loans to SHGs",
        "benefits_ta": "சுயஉதவி குழுக்களுக்கு பிணையம் இல்லாத கடன்கள்",
        "eligibility": ["Women in SHGs"],
        "type": "Women Empowerment",
        "type_ta": "பெண்கள் அதிகாரமளித்தல்",
        "link": "https://aajeevika.gov.in/",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "nabard_women",
        "name": "NABARD Women Farmer Support",
        "name_ta": "நபார்டு பெண் விவசாயி ஆதரவு",
        "description": "Subsidies and loans for women SHGs and agri businesses",
        "description_ta": "பெண் குழுக்களுக்கான மானியங்கள் மற்றும் கடன்கள்",
        "benefits": "Grant assistance for skill development",
        "benefits_ta": "திறன் மேம்பாட்டிற்கு மானிய உதவி",
        "eligibility": ["Women farmers/entrepreneurs"],
        "type": "Women Empowerment",
        "type_ta": "பெண்கள் அதிகாரமளித்தல்",
        "link": "https://www.nabard.org/content1.aspx?cid=506&id=23",
        "adoption_level": ["Moderate", "High"]
    },
    {
        "id": "namo_drone_didi",
        "name": "Namo Drone Didi Scheme",
        "name_ta": "நமோ ட்ரோன் திதி திட்டம்",
        "description": "Drones to women SHGs with heavy subsidy (80% cost assistance)",
        "description_ta": "பெண் குழுக்களுக்கு 80% மானியத்துடன் ட்ரோன்கள்",
        "benefits": "New livelihood opportunities using drones",
        "benefits_ta": "ட்ரோன்கள் மூலம் புதிய வாழ்வாதார வாய்ப்புகள்",
        "eligibility": ["Women SHGs"],
        "type": "Technology",
        "type_ta": "தொழில்நுட்பம்",
        "link": "https://pib.gov.in/PressReleaseIframePage.aspx?PRID=1980689",
        "adoption_level": ["High"]
    },
    {
        "id": "women_subsidy",
        "name": "Extra Subsidy Incentives for Women Farmers",
        "name_ta": "பெண் விவசாயிகளுக்கு கூடுதல் மானிய சலுகைகள்",
        "description": "Higher subsidies or priority in many TN and central schemes",
        "description_ta": "பல திட்டங்களில் அதிக மானியங்கள் அல்லது முன்னுரிமை",
        "benefits": "Additional 10-20% subsidy in some schemes",
        "benefits_ta": "சில திட்டங்களில் கூடுதல் 10-20% மானியம்",
        "eligibility": ["Women farmers"],
        "type": "Subsidy",
        "type_ta": "மானியம்",
        "link": "https://tnagrisnet.tn.gov.in/",
        "adoption_level": ["Low", "Moderate", "High"]
    }
]

# Digital Platforms / Apps for Farmers
DIGITAL_PLATFORMS = [
    {
        "id": "uzhavar_santhai",
        "name": "Uzhavar Santhai (TN Farmer Market Initiative)",
        "name_ta": "உழவர் சந்தை",
        "description": "Direct farmer-to-consumer market",
        "description_ta": "நேரடி விவசாயி-நுகர்வோர் சந்தை",
        "benefits": "Eliminates middlemen, better returns",
        "benefits_ta": "இடைத்தரகர்கள் இல்லை, சிறந்த லாபம்",
        "eligibility": ["TN Farmers"],
        "type": "Market",
        "type_ta": "சந்தை",
        "link": "https://www.tnmsc.com/uzhavar-santhai.php",
        "adoption_level": ["Low", "Moderate", "High"]
    },
    {
        "id": "grains_portal",
        "name": "GRAINS Portal (Grower Registration System)",
        "name_ta": "கிரைன்ஸ் போர்டல்",
        "description": "Single digital platform for TN farmers",
        "description_ta": "தமிழ்நாடு விவசாயிகளுக்கான ஒற்றை டிஜிட்டல் தளம்",
        "benefits": "Easy access to multiple schemes",
        "benefits_ta": "பல திட்டங்களுக்கு எளிதான அணுகல்",
        "eligibility": ["All TN Farmers"],
        "type": "Digital Service",
        "type_ta": "டிஜிட்டல் சேவை",
        "link": "https://grains.tn.gov.in/",
        "adoption_level": ["Moderate", "High"]
    },
    {
        "id": "agristack",
        "name": "Agristack Tamil Nadu / Digital Database",
        "name_ta": "அக்ரிஸ்டாக் தமிழ்நாடு / டிஜிட்டல் தரவுத்தளம்",
        "description": "Farmer database for scheme access and forecasts",
        "description_ta": "திட்ட அணுகல் மற்றும் கணிப்புகளுக்கான விவசாயி தரவுத்தளம்",
        "benefits": "Proactive service delivery",
        "benefits_ta": "சுறுசுறுப்பான சேவை வழங்கல்",
        "eligibility": ["Registered Farmers"],
        "type": "Digital Service",
        "type_ta": "டிஜிட்டல் சேவை",
        "link": "https://agristack.gov.in/",
        "adoption_level": ["Moderate", "High"]
    },
    {
        "id": "namma_arasu",
        "name": "Namma Arasu Chatbot",
        "name_ta": "நம்ம அரசு சாட்போட்",
        "description": "WhatsApp/chatbot access to many schemes",
        "description_ta": "பல திட்டங்களுக்கு வாட்ஸ்அப் வழியாக அணுகல்",
        "benefits": "Information at fingertips",
        "benefits_ta": "விரல் நுனியில் தகவல்",
        "eligibility": ["Anyone"],
        "type": "Information",
        "type_ta": "தகவல்",
        "link": "https://www.tn.gov.in/tnchatbot/",
        "adoption_level": ["Low", "Moderate", "High"]
    }
]

def get_all_schemes():
    return CENTRAL_SCHEMES + TAMIL_NADU_SCHEMES + WOMEN_SCHEMES + DIGITAL_PLATFORMS

def filter_schemes_by_eligibility(farmer_data):
    all_schemes = get_all_schemes()
    eligible_schemes = []

    adoption_category = farmer_data.get('adoption_category', 'Moderate')
    
    if 'High' in adoption_category: adoption_category = 'High'
    elif 'Moderate' in adoption_category: adoption_category = 'Moderate'
    else: adoption_category = 'Low'
        
    gender = farmer_data.get('gender', 'Male')

    for scheme in all_schemes:
        is_relevant = True
        
        if 'adoption_level' in scheme and adoption_category not in scheme['adoption_level']:
            is_relevant = False
            
        if scheme.get('type') == 'Women Empowerment' and gender != 'Female':
            is_relevant = False

        if is_relevant:
            eligible_schemes.append(scheme)
            
    return eligible_schemes
