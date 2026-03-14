import numpy as np
import joblib
import pandas as pd
import os

class RecommendationEngine:
    def __init__(self):
        # Paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.crop_model_path = os.path.join(self.current_dir, 'crop_model.pkl')
        self.encoders_path = os.path.join(self.current_dir, 'encoders.pkl')
        
        # Load ML model and encoders
        try:
            self.model = joblib.load(self.crop_model_path)
            self.encoders = joblib.load(self.encoders_path)
            self.has_ml = True
            print("ML Crop Recommendation model loaded successfully in recommendation.py")
        except:
            self.has_ml = False
            print("ML Crop model not found, falling back to rule-based")
            
        # Specified crop ml features
        self.crop_features = ['soil_type', 'water_availability', 'irrigation_method', 'season', 'land_area', 'crop_type']

        # Technology Details Database
        self.tech_details = {
            'Agricultural Drone': {
                'name_en': 'Agricultural Drone', 'name_ta': 'விவசாய ட்ரோன்',
                'description_en': 'For efficient pesticide spraying and monitoring.',
                'description_ta': 'பூச்சிக்கொல்லி தெளித்தல் மற்றும் கண்காணிப்புக்கு.',
                'cost_en': '₹1,50,000+', 'cost_ta': '₹1,50,000+',
                'scheme_en': 'Namo Drone Didi / SMAM', 'scheme_ta': 'ட்ரோன் திதி / SMAM'
            },
            'IoT Soil Sensors': {
                'name_en': 'IoT Soil Sensors', 'name_ta': 'IoT மண் சென்சார்கள்',
                'description_en': 'Real-time soil moisture and nutrient monitoring.',
                'description_ta': 'உண்நேர மண் ஈரப்பதம் மற்றும் ஊட்டச்சத்து கண்காணிப்பு.',
                'cost_en': '₹5,000 - ₹20,000', 'cost_ta': '₹5,000 - ₹20,000',
                'scheme_en': 'Digital Agriculture Mission', 'scheme_ta': 'டிஜிட்டல் வேளாண்மை திட்டம்'
            },
            'Precision Agriculture Tools': {
                'name_en': 'Precision Agriculture Tools', 'name_ta': 'துல்லியமான வேளாண்மை கருவிகள்',
                'description_en': 'GPS guided optimization of field variability.',
                'description_ta': 'ஜிபிஎஸ் மூலம் புல மாறுபாட்டை மேம்படுத்துதல்.',
                'cost_en': '₹50,000+', 'cost_ta': '₹50,000+',
                'scheme_en': 'RKVY-RAFTAAR', 'scheme_ta': 'RKVY-RAFTAAR'
            },
            'Smart Greenhouse System': {
                'name_en': 'Smart Greenhouse System', 'name_ta': 'ஸ்மார்ட் பசுமை இல்லம்',
                'description_en': 'Automated climate control for high-value crops.',
                'description_ta': 'அதிக மதிப்புள்ள பயிர்களுக்கு தானியங்கி காலநிலை கட்டுப்பாடு.',
                'cost_en': '₹2,00,000+', 'cost_ta': '₹2,00,000+',
                'scheme_en': 'National Horticulture Board', 'scheme_ta': 'தேசிய தோட்டக்கலை வாரியம்'
            },
            'AI Crop Monitoring': {
                'name_en': 'AI Crop Monitoring', 'name_ta': 'AI பயிர் கண்காணிப்பு',
                'description_en': 'AI powered disease and health monitoring.',
                'description_ta': 'AI மூலம் நோய்கள் மற்றும் சுகாதார கண்காணிப்பு.',
                'cost_en': 'Subscription Based', 'cost_ta': 'சந்தா அடிப்படையில்',
                'scheme_en': 'AgriStack Mission', 'scheme_ta': 'AgriStack திட்டம்'
            },
            'Drip Irrigation': {
                'name_en': 'Drip Irrigation', 'name_ta': 'சொட்டு நீர் பாசனம்',
                'description_en': 'Saves 40-60% water, increases yield.',
                'description_ta': '40-60% தண்ணீரைச் சேமிக்கிறது, மகசூலை அதிகரிக்கிறது.',
                'cost_en': '₹40,000 - ₹80,000 per acre', 'cost_ta': 'ஏக்கருக்கு ₹40,000 - ₹80,000',
                'scheme_en': 'PMKSY / TN Micro Irrigation', 'scheme_ta': 'PMKSY / நுண்ணீர் பாசன மானியம்'
            },
            'Soil Testing Kit': {
                'name_en': 'Soil Testing Kit', 'name_ta': 'மண் பரிசோதனை கருவி',
                'description_en': 'Check soil NPK and pH levels instantly.',
                'description_ta': 'மண் NPK மற்றும் pH அளவுகளை உடனடியாகச் சரிபார்க்கவும்.',
                'cost_en': '₹1,500 - ₹3,000', 'cost_ta': '₹1,500 - ₹3,000',
                'scheme_en': 'Soil Health Card Scheme', 'scheme_ta': 'மண் ஆரோக்கிய அட்டை திட்டம்'
            },
            'Mobile Agri Apps': {
                'name_en': 'Mobile Agri Apps', 'name_ta': 'மொபைல் வேளாண் செயலிகள்',
                'description_en': 'Advisory, weather, and market price tracking.',
                'description_ta': 'ஆலோசனை, வானிலை, மற்றும் சந்தை விலை தரவு பயன்பாடுகள்.',
                'cost_en': 'Free / Low Cost', 'cost_ta': 'இலவசம்',
                'scheme_en': 'Digital India Agriculture', 'scheme_ta': 'டிஜிட்டல் இந்தியா வேளாண்மை'
            },
            'Crop Advisory Systems': {
                'name_en': 'Crop Advisory Systems', 'name_ta': 'பயிர் ஆலோசனை அமைப்புகள்',
                'description_en': 'Expert guidelines tailored to your farm.',
                'description_ta': 'உங்கள் பண்ணைக்கான நிபுணர்களின் வழிகாட்டுதல்கள்.',
                'cost_en': 'Free', 'cost_ta': 'இலவசம்',
                'scheme_en': 'Kisan Suvidha', 'scheme_ta': 'கிசான் சுவிதா'
            },
            'Sprinkler Irrigation': {
                'name_en': 'Sprinkler Irrigation', 'name_ta': 'தெளிப்பு நீர் பாசனம்',
                'description_en': 'Suitable for close growing crops like pulses.',
                'description_ta': 'பயறு வகைகள் போன்ற நெருக்கமாக வளரும் பயிர்களுக்கு ஏற்றது.',
                'cost_en': '₹20,000 - ₹50,000 per acre', 'cost_ta': 'ஏக்கருக்கு ₹20,000 - ₹50,000',
                'scheme_en': 'PMKSY / PM-Krishi Sinchai', 'scheme_ta': 'பிஎம் கிரிஷி சின்சாயி'
            },
            'Basic Irrigation Improvements': {
                'name_en': 'Basic Irrigation Improvements', 'name_ta': 'அடிப்படை நீர்ப்பாசன மேம்பாடுகள்',
                'description_en': 'Low cost improvements for better water use.',
                'description_ta': 'சிறந்த நீர் பயன்பாட்டிற்கான குறைந்த செலவிலான மேம்பாடுகள்.',
                'cost_en': '₹5,000 - ₹10,000', 'cost_ta': '₹5,000 - ₹10,000',
                'scheme_en': 'Kalaignar Scheme', 'scheme_ta': 'கலைஞர் திட்டம்'
            },
            'Government Training Programs': {
                'name_en': 'Government Training Programs', 'name_ta': 'அரசு பயிற்சி திட்டங்கள்',
                'description_en': 'Extensive training provided by agriculture departments.',
                'description_ta': 'வேளாண்மை துறைகள் மூலம் வழங்கப்படும் விரிவான பயிற்சி.',
                'cost_en': 'Free', 'cost_ta': 'இலவசம்',
                'scheme_en': 'NMAET / ATMA', 'scheme_ta': 'NMAET / ATMA'
            },
            'Subsidized Equipment': {
                'name_en': 'Subsidized Equipment', 'name_ta': 'மானிய உபகரணங்கள்',
                'description_en': 'Essential low cost tools for farming.',
                'description_ta': 'பண்ணைக்கான அன்றாட பயன்பாட்டு குறைந்த செலவு உபகரணங்கள்.',
                'cost_en': '50% Subsidy', 'cost_ta': '50% மானியம்',
                'scheme_en': 'Farm Mechanization', 'scheme_ta': 'வேளாண் இயந்திரமயமாக்கல்'
            },
            'Farmer Extension Services': {
                'name_en': 'Farmer Extension Services', 'name_ta': 'விவசாய நீட்டிப்பு சேவைகள்',
                'description_en': 'Support and assistance through local centers.',
                'description_ta': 'உள்ளூர் மையங்கள் மூலம் ஆதரவு மற்றும் உதவி.',
                'cost_en': 'Free', 'cost_ta': 'இலவசம்',
                'scheme_en': 'State Extension Services', 'scheme_ta': 'மாநில விரிவாக்க சேவைகள்'
            }
        }

        # 1. Technology Hierarchies
        self.technology_recommendations = {
            'High': ['Agricultural Drone', 'IoT Soil Sensors', 'Precision Agriculture Tools', 'AI Crop Monitoring', 'Smart Greenhouse System'],
            'Medium': ['Drip Irrigation', 'Soil Testing Kit', 'Mobile Agri Apps', 'Crop Advisory Systems', 'Sprinkler Irrigation'],
            'Low': ['Basic Irrigation Improvements', 'Government Training Programs', 'Subsidized Equipment', 'Farmer Extension Services']
        }
        
        # 2. Crop Database
        self.crop_database = {
            'Rice': {'crop_en': 'Rice', 'crop_ta': 'நெல்/அரிசி', 'technologies': ['Transplanter']},
            'Sugarcane': {'crop_en': 'Sugarcane', 'crop_ta': 'கரும்பு', 'technologies': ['Drip']},
            'Banana': {'crop_en': 'Banana', 'crop_ta': 'வாழை', 'technologies': ['Propping', 'Drip']},
            'Cotton': {'crop_en': 'Cotton', 'crop_ta': 'பருத்தி', 'technologies': ['Sprayer']},
            'Turmeric': {'crop_en': 'Turmeric', 'crop_ta': 'மஞ்சள்', 'technologies': ['Boiler']},
            'Maize': {'crop_en': 'Maize', 'crop_ta': 'மக்காச்சோளம்', 'technologies': ['Sheller']},
            'Chillies': {'crop_en': 'Chillies', 'crop_ta': 'மிளகாய்', 'technologies': ['Solar Dryer']},
            'Coconut': {'crop_en': 'Coconut', 'crop_ta': 'தென்னை/தேங்காய்', 'technologies': ['Tree Climber', 'Drip']},
            'Groundnut': {'crop_en': 'Groundnut', 'crop_ta': 'வேர்க்கடலை', 'technologies': ['Decorticator']},
            'Pulses': {'crop_en': 'Pulses', 'crop_ta': 'பயறு வகைகள்', 'technologies': ['Sprinkler']},
            'Millets': {'crop_en': 'Millets', 'crop_ta': 'சிறு தானியங்கள்', 'technologies': ['Dehuller']},
            'Tomato': {'crop_en': 'Tomato', 'crop_ta': 'தக்காளி', 'technologies': ['Drip']},
            'Watermelon': {'crop_en': 'Watermelon', 'crop_ta': 'தர்பூசணி', 'technologies': ['Drip']}
        }

        # 3. Schemes Database
        self.schemes_database = [
            {
                'id': 'PM-KISAN', 'name_en': 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)', 'name_ta': 'பிஎம்-கிசான்',
                'desc_en': 'Financial support of Rs. 6000 per year for small and marginal farmers.',
                'desc_ta': 'சிறு மற்றும் குறு விவசாயிகளுக்கு ஆண்டுக்கு ரூ. 6000 நிதியுதவி.',
                'condition': lambda d: float(d.get('land_area') or 2) <= 5
            },
            {
                'id': 'PMKSY', 'name_en': 'PMKSY (Pradhan Mantri Krishi Sinchayee Yojana)', 'name_ta': 'பிஎம்கேஎஸ்ஒய்',
                'desc_en': 'Subsidy for Micro Irrigation like Drip and Sprinkler.',
                'desc_ta': 'சொட்டு நீர் மற்றும் தெளிப்பு நீர் பாசனத்திற்கான மானியம்.',
                'condition': lambda d: d.get('irrigation_source') in ['Borewell', 'Canal', 'River', 'Farm Pond']
            },
            {
                'id': 'KCC', 'name_en': 'Kisan Credit Card (KCC)', 'name_ta': 'கிசான் கிரெடிட் கார்டு',
                'desc_en': 'Short-term credit limits for crop needs and expenses.',
                'desc_ta': 'பயிர் தேவைகள் மற்றும் செலவுகளுக்கான குறுகிய கால கடன் வசதி.',
                'condition': lambda d: d.get('has_loan') == True or d.get('access_to_credit', 'No') == 'No'
            },
            {
                'id': 'PMFBY', 'name_en': 'PMFBY (Pradhan Mantri Fasal Bima Yojana)', 'name_ta': 'பிஎம்எஃப்பிஒய் (பயிர் காப்பீடு)',
                'desc_en': 'Crop insurance scheme covering yield losses due to non-preventable risks.',
                'desc_ta': 'தவிர்க்க முடியாத அபாயங்களால் ஏற்படும் மகசூல் இழப்புகளை உள்ளடக்கக்கூடிய பயிர் காப்பீட்டு திட்டம்.',
                'condition': lambda d: d.get('has_insurance') == False or str(d.get('insurance')).lower() == 'no'
            },
            {
                'id': 'MahilaKisan', 'name_en': 'Mahila Kisan Sashaktikaran Pariyojana (MKSP)', 'name_ta': 'மகிளா கிசான் திட்டம்',
                'desc_en': 'Empowering women in agriculture through capacity building.',
                'desc_ta': 'விவசாயத்தில் பெண்களை அதிகாரபூர்வமாக்கும் திட்டம்.',
                'condition': lambda d: str(d.get('gender')).lower() == 'female'
            },
            {
                'id': 'NRLM', 'name_en': 'Deendayal Antyodaya Yojana-NRLM', 'name_ta': 'தீன்தயாள் திட்டம்-NRLM',
                'desc_en': 'Targeted at women-led self-help groups in rural farming sectors.',
                'desc_ta': 'விவசாயத்தில் உள்ள மகளிர் சுய உதவிக் குழுக்களுக்கான ஆதரவு.',
                'condition': lambda d: str(d.get('gender')).lower() == 'female'
            },
            {
                'id': 'UzhavarSandhai', 'name_en': 'Uzhavar Sandhai (Tamil Nadu Farmer Market)', 'name_ta': 'உழவர் சந்தை',
                'desc_en': 'Direct selling platform for Tamil Nadu farmers.',
                'desc_ta': 'விவசாயிகள் நேரடியாக விற்பனை செய்ய உழவர் சந்தை திட்டம்.',
                'condition': lambda d: str(d.get('state', '')).lower() == 'tamil nadu' or d.get('sells_in_uzhavar_santhai', False)
            },
            {
                'id': 'AIF', 'name_en': 'Agriculture Infrastructure Fund', 'name_ta': 'வேளாண் உள்கட்டமைப்பு நிதி',
                'desc_en': 'Funding for post-harvest management infrastructure.',
                'desc_ta': 'அறுவடைக்கு பிந்தைய மேலாண்மைக்கான நிதி.',
                'condition': lambda d: float(d.get('land_area') or 2) >= 5
            },
            {
                'id': 'PKVY', 'name_en': 'Paramparagat Krishi Vikas Yojana', 'name_ta': 'பாரம்பரிய வேளாண்மை திட்டம்',
                'desc_en': 'Promotes organic farming through cluster approach.',
                'desc_ta': 'குழு முறையில் இயற்கை விவசாயத்தை ஊக்குவிக்கிறது.',
                'condition': lambda d: True # Universal fallback
            }
        ]

    def _safe_encode(self, col, val):
        if col not in self.encoders:
            return val
        le = self.encoders[col]
        str_val = str(val) if val is not None and str(val).strip() != "" else le.classes_[0]
        if str_val not in le.classes_:
            str_val = le.classes_[0]
        return le.transform([str_val])[0]
        
    def _safe_float(self, val, default):
        try:
            return float(val) if val is not None and str(val).strip() != "" else default
        except:
            return default

    def get_technology_recommendations(self, farmer_data):
        adoption_category = farmer_data.get('adoption_category', 'Medium')
        existing_tech = farmer_data.get('technologies_used', [])
        
        if 'High' in adoption_category: target_cat = 'High'
        elif 'Low' in adoption_category: target_cat = 'Low'
        else: target_cat = 'Medium'
        
        base_tech_names = self.technology_recommendations.get(target_cat, [])
        
        recommendations = []
        for tech_name in base_tech_names:
            # Skip if farmer is already using this technology
            if tech_name in existing_tech or tech_name.replace(' ', '') in [t.replace(' ', '') for t in existing_tech]:
                continue
                
            details = self.tech_details.get(tech_name, {})
            recommendations.append({
                'tech_en': details.get('name_en', tech_name),
                'tech_ta': details.get('name_ta', tech_name),
                'description_en': details.get('description_en', ''),
                'description_ta': details.get('description_ta', ''),
                'cost_en': details.get('cost_en', 'N/A'),
                'cost_ta': details.get('cost_ta', 'N/A'),
                'scheme_en': details.get('scheme_en', 'N/A'),
                'scheme_ta': details.get('scheme_ta', 'N/A')
            })
            
        return recommendations[:5]
    
    def get_crop_recommendations(self, farmer_data):
        if self.has_ml:
            try:
                # Prepare features - Map from DB schema to ML feature names
                data = {}
                data['land_area'] = self._safe_float(farmer_data.get('land_area'), 2.0)
                data['soil_type'] = farmer_data.get('soil_type', 'Red')
                data['water_availability'] = farmer_data.get('water_availability', 'Medium')
                
                # Derive crop_type from crops list
                crops_list = farmer_data.get('crops', [])
                data['crop_type'] = crops_list[0] if crops_list and len(crops_list) > 0 else 'Cash Crop'
                
                # Map irrigation_source to irrigation_method if missing
                data['irrigation_method'] = farmer_data.get('irrig_method') or farmer_data.get('irrigation_source') or 'Rainfed'
                data['season'] = farmer_data.get('season', 'Kharif')

                encoded_data = {}
                for col in self.crop_features:
                    if col in self.encoders:
                        encoded_data[col] = self._safe_encode(col, data.get(col))
                    else:
                        encoded_data[col] = data.get(col)

                X_input = pd.DataFrame([encoded_data])
                probs = self.model.predict_proba(X_input)[0]
                
                crop_le = self.encoders['crop_recommendation']
                top_indices = np.argsort(probs)[-4:][::-1]
                
                recommended_crops = []
                for idx in top_indices:
                    crop_name = crop_le.inverse_transform([idx])[0]
                    details = self.crop_database.get(crop_name)
                    if details:
                        recommended_crops.append({
                            'crop_en': details['crop_en'],
                            'crop_ta': details['crop_ta'],
                            'reason_en': "ML predicted based on your unique combination of soil, water, and behavioral features.",
                            'reason_ta': "உங்கள் மண், நீர் மற்றும் மேலாண்மை விவரங்களைக் கொண்டு செயற்கை நுண்ணறிவு மூலம் கணிக்கப்பட்டது.",
                            'technologies': details.get('technologies', [])
                        })
                
                if len(recommended_crops) >= 2:
                    return recommended_crops[:4]
            except Exception as e:
                print(f"ML Prediction failed: {e}")

        # Fallback specific logic
        return [
            {'crop_en': 'Groundnut', 'crop_ta': 'வேர்க்கடலை', 'reason_en': 'Suitable based on general logic.', 'reason_ta': 'பொதுவான காரணத்தால் ஏற்றது.'},
            {'crop_en': 'Maize', 'crop_ta': 'மக்காச்சோளம்', 'reason_en': 'Good yield.', 'reason_ta': 'நல்ல மகசூல்.'}
        ]

    def get_all_recommendations(self, farmer_data):
        return {
            'technologies': self.get_technology_recommendations(farmer_data),
            'crops': self.get_crop_recommendations(farmer_data)
        }

recommendation_engine = RecommendationEngine()

