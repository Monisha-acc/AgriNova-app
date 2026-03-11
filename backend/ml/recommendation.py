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
            print("ML Crop Recommendation model loaded successfully")
        except:
            self.has_ml = False
            print("ML Crop model not found, falling back to rule-based")
            
        # Feature order for the model
        self.feature_order = [
            'soil_type', 'irrigation_source', 'land_area', 'water_availability',
            'crop_type', 'crop_rotation', 'seasonal_crop', 'irrigation_method',
            'irrigation_frequency', 'water_source', 'water_storage',
            'access_to_credit', 'insurance', 'subsidy_usage',
            'sells_in_uzhavar_santhai', 'uses_enam', 'drip_irrigation',
            'sprinkler_irrigation', 'rainwater_harvesting',
            'soil_moisture_monitoring', 'attended_training',
            'smartphone_usage', 'agri_apps_usage'
        ]
        # Technology Details Database
        self.tech_details = {
            'Agricultural Drone': {
                'name_en': 'Agricultural Drone',
                'name_ta': 'விவசாய ட்ரோன்',
                'description_en': 'For efficient pesticide spraying and monitoring.',
                'description_ta': 'பூச்சிக்கொல்லி தெளித்தல் மற்றும் கண்காணிப்புக்கு.',
                'cost_en': 'Cost: ₹5 Lakhs - ₹10 Lakhs',
                'cost_ta': 'செலவு: ₹5 லட்சம் - ₹10 லட்சம்',
                'subsidy_en': '40-50% Subsidy available',
                'subsidy_ta': '40-50% மானியம் கிடைக்கும்'
            },
            'IoT Soil Sensors': {
                'name_en': 'IoT Soil Sensors',
                'name_ta': 'IoT மண் சென்சார்கள்',
                'description_en': 'Real-time soil moisture and nutrient monitoring.',
                'description_ta': 'உண்நேர மண் ஈரப்பதம் மற்றும் ஊட்டச்சத்து கண்காணிப்பு.',
                'cost_en': 'Cost: ₹15,000 - ₹50,000',
                'cost_ta': 'செலவு: ₹15,000 - ₹50,000',
                'subsidy_en': 'Part of Smart Farming schemes',
                'subsidy_ta': 'ஸ்மார்ட் விவசாயத் திட்டங்களின் ஒரு பகுதி'
            },
            'Precision Agriculture Tools': {
                'name_en': 'Precision Agriculture Tools',
                'name_ta': 'துல்லியமான வேளாண்மை கருவிகள்',
                'description_en': 'GPS guided optimization of field variability.',
                'description_ta': 'ஜிபிஎஸ் மூலம் புல மாறுபாட்டை மேம்படுத்துதல்.',
                'cost_en': 'Cost: Varies',
                'cost_ta': 'செலவு: மாறுபடும்',
                'subsidy_en': 'Project based',
                'subsidy_ta': 'திட்டம் சார்ந்தது'
            },
            'Smart Greenhouse System': {
                'name_en': 'Smart Greenhouse System',
                'name_ta': 'ஸ்மார்ட் பசுமை இல்லம்',
                'description_en': 'Automated climate control for high-value crops.',
                'description_ta': 'அதிக மதிப்புள்ள பயிர்களுக்கு தானியங்கி காலநிலை கட்டுப்பாடு.',
                'cost_en': 'Cost: ₹1000/sq.m onwards',
                'cost_ta': 'செலவு: ₹1000/ச.மீ முதல்',
                'subsidy_en': '50% under NHM',
                'subsidy_ta': 'NHM கீழ் 50%'
            },
            'Auto Irrigation Controller': {
                'name_en': 'Auto Irrigation Controller',
                'name_ta': 'தானியங்கி நீர்ப்பாசன கட்டுப்பாட்டாளர்',
                'description_en': 'Schedule watering automatically via mobile.',
                'description_ta': 'மொபைல் மூலம் தானாகவே நீர்ப்பாசனத்தை திட்டமிடலாம்.',
                'cost_en': 'Cost: ₹5,000 - ₹20,000',
                'cost_ta': 'செலவு: ₹5,000 - ₹20,000',
                'subsidy_en': 'Included in Micro Irrigation',
                'subsidy_ta': 'நுண்ணீர் பாசனத்தில் சேர்க்கப்பட்டுள்ளது'
            },
            'Hydroponics System': {
                'name_en': 'Hydroponics System',
                'name_ta': 'ஹைட்ரோபோனிக்ஸ் அமைப்பு',
                'description_en': 'Soil-less farming for high yield.',
                'description_ta': 'அதிக மகசூலுக்கான மண் இல்லாத விவசாயம்.',
                'cost_en': 'Cost: ₹5 Lakhs onwards',
                'cost_ta': 'செலவு: ₹5 லட்சம் முதல்',
                'subsidy_en': 'Back-ended subsidy available',
                'subsidy_ta': 'பின்முனை மானியம் கிடைக்கும்'
            },
            'Drip Irrigation': {
                'name_en': 'Drip Irrigation',
                'name_ta': 'சொட்டு நீர் பாசனம்',
                'description_en': 'Saves 40-60% water, increases yield.',
                'description_ta': '40-60% தண்ணீரைச் சேமிக்கிறது, மகசூலை அதிகரிக்கிறது.',
                'cost_en': 'Cost: ₹45,000/acre',
                'cost_ta': 'செலவு: ₹45,000/ஏக்கர்',
                'subsidy_en': '100% for Small/Marginal, 75% for others',
                'subsidy_ta': 'சிறு/குறு விவசாயிகளுக்கு 100%, மற்றவர்களுக்கு 75%'
            },
            'Sprinkler Irrigation': {
                'name_en': 'Sprinkler Irrigation',
                'name_ta': 'தெளிப்பு நீர் பாசனம்',
                'description_en': 'Suitable for close growing crops like pulses.',
                'description_ta': 'பயறு வகைகள் போன்ற நெருக்கமாக வளரும் பயிர்களுக்கு ஏற்றது.',
                'cost_en': 'Cost: ₹20,000/acre',
                'cost_ta': 'செலவு: ₹20,000/ஏக்கர்',
                'subsidy_en': '75% Subsidy',
                'subsidy_ta': '75% மானியம்'
            },
            'Soil Testing Kit': {
                'name_en': 'Soil Testing Kit',
                'name_ta': 'மண் பரிசோதனை கருவி',
                'description_en': 'Check soil NPK and pH levels instantly.',
                'description_ta': 'மண் NPK மற்றும் pH அளவுகளை உடனடியாகச் சரிபார்க்கவும்.',
                'cost_en': 'Cost: ₹2,000 - ₹5,000',
                'cost_ta': 'செலவு: ₹2,000 - ₹5,000',
                'subsidy_en': 'Available at KVKs',
                'subsidy_ta': 'KVK-களில் கிடைக்கும்'
            },
            'Power Tiller': {
                'name_en': 'Power Tiller',
                'name_ta': 'விசை உழுவை',
                'description_en': 'For ploughing and weeding in small farms.',
                'description_ta': 'சிறு பண்ணைகளில் உழுதல் மற்றும் களை எடுப்பதற்கு.',
                'cost_en': 'Cost: ₹1.5 Lakhs - ₹2 Lakhs',
                'cost_ta': 'செலவு: ₹1.5 லட்சம் - ₹2 லட்சம்',
                'subsidy_en': '40-50% Subsidy',
                'subsidy_ta': '40-50% மானியம்'
            },
            'Solar Water Pump': {
                'name_en': 'Solar Water Pump',
                'name_ta': 'சூரிய சக்தி நீர் பம்பி',
                'description_en': 'Eco-friendly irrigation without electricity bills.',
                'description_ta': 'மின்சாரக் கட்டணம் இல்லாத சூழல் நட்பு நீர்ப்பாசனம்.',
                'cost_en': 'Cost: ₹2 Lakhs - ₹5 Lakhs',
                'cost_ta': 'செலவு: ₹2 லட்சம் - ₹5 லட்சம்',
                'subsidy_en': 'up to 60% under PM-KUSUM',
                'subsidy_ta': 'PM-KUSUM கீழ் 60% வரை'
            },
            'Mini Tractor': {
                'name_en': 'Mini Tractor',
                'name_ta': 'சிறிய டிராக்டர்',
                'description_en': 'Ideal for orchards and inter-culture operations.',
                'description_ta': 'தோப்புகள் மற்றும் இடைக்கால நடவடிக்கைகளுக்கு சிறந்தது.',
                'cost_en': 'Cost: ₹3 Lakhs - ₹5 Lakhs',
                'cost_ta': 'செலவு: ₹3 லட்சம் - ₹5 லட்சம்',
                'subsidy_en': 'Subject to availability',
                'subsidy_ta': 'கிடைப்பதைப் பொறுத்தது'
            },
            'Seed Drill': {
                'name_en': 'Seed Drill',
                'name_ta': 'விதைக்கும் கருவி',
                'description_en': 'For proper line sowing and seed saving.',
                'description_ta': 'சரியான வரிசை விதைப்பு மற்றும் விதை சேமிப்பிற்கு.',
                'cost_en': 'Cost: ₹15,000 - ₹40,000',
                'cost_ta': 'செலவு: ₹15,000 - ₹40,000',
                'subsidy_en': '40% Subsidy',
                'subsidy_ta': '40% மானியம்'
            },
            'Basic Drip Kit': {
                'name_en': 'Basic Drip Kit',
                'name_ta': 'எளிய சொட்டு நீர் கருவி',
                'description_en': 'Low cost drip for small vegetable gardens.',
                'description_ta': 'சிறிய காய்கறி தோட்டங்களுக்கு குறைந்த செலவிலான சொட்டு நீர் பாசன அமைப்பு.',
                'cost_en': 'Cost: ₹2,000 - ₹5,000',
                'cost_ta': 'செலவு: ₹2,000 - ₹5,000',
                'subsidy_en': 'None',
                'subsidy_ta': 'திட்டம் இல்லை'
            },
            'Manual Sprayer': {
                'name_en': 'Manual Sprayer',
                'name_ta': 'கையால் இயக்கும் தெளிப்பான்',
                'description_en': 'Essential for plant protection.',
                'description_ta': 'தாவர பாதுகாப்புக்கு இன்றியமையாதது.',
                'cost_en': 'Cost: ₹2,000',
                'cost_ta': 'செலவு: ₹2,000',
                'subsidy_en': '50% Subsidy',
                'subsidy_ta': '50% மானியம்'
            },
            'Vermicompost Unit': {
                'name_en': 'Vermicompost Unit',
                'name_ta': 'மண்புழு உர அலகு',
                'description_en': 'Turn farm waste into rich fertilizer.',
                'description_ta': 'பண்ணை கழிவுகளை செழுமையான உரமாக மாற்றவும்.',
                'cost_en': 'Cost: ₹10,000 (Construction)',
                'cost_ta': 'செலவு: ₹10,000 (கட்டுமானம்)',
                'subsidy_en': 'Support under NHM',
                'subsidy_ta': 'NHM கீழ் ஆதரவு'
            },
            'Improved Seeds': {
                'name_en': 'Improved Seeds',
                'name_ta': 'மேம்படுத்தப்பட்ட விதைகள்',
                'description_en': 'High yielding and disease resistant varieties.',
                'description_ta': 'அதிக மகசூல் தரும் மற்றும் நோய் எதிர்ப்புத் திறன் கொண்ட ரகங்கள்.',
                'cost_en': 'Cost: Subsidized rates',
                'cost_ta': 'செலவு: மானிய விலையில்',
                'subsidy_en': 'Available at Agr. Depots',
                'subsidy_ta': 'விவசாயக் கிடங்குகளில் கிடைக்கும்'
            },
            'Tarpaulin Sheets': {
                'name_en': 'Tarpaulin Sheets',
                'name_ta': 'தார்பாய் விரிப்புகள்',
                'description_en': 'For drying crops and protection from rain.',
                'description_ta': 'பயிர்களை உலர்த்துவதற்கும் மழையிலிருந்து பாதுகாப்பதற்கும்.',
                'cost_en': 'Cost: ₹1,500 - ₹3,000',
                'cost_ta': 'செலவு: ₹1,500 - ₹3,000',
                'subsidy_en': '50% Subsidy',
                'subsidy_ta': '50% மானியம்'
            }
        }

        # 1. Technology Hierarchies STRICTLY by adoption category
        self.technology_recommendations = {
            'High': [
                'Agricultural Drone', 'IoT Soil Sensors', 'Precision Agriculture Tools', 
                'Smart Greenhouse System', 'Auto Irrigation Controller', 'Hydroponics System'
            ],
            'Moderate': [
                'Drip Irrigation', 'Sprinkler Irrigation', 'Soil Testing Kit', 
                'Power Tiller', 'Solar Water Pump', 'Mini Tractor', 'Seed Drill'
            ],
            'Low': [
                'Basic Drip Kit', 'Manual Sprayer', 'Vermicompost Unit', 
                'Improved Seeds', 'Tarpaulin Sheets'
            ]
        }
        
        # 2. Crop Database: STRICTLY mapped to Soil and Water
        self.crop_database = {
            'Rice': {
                'crop_en': 'Rice',
                'crop_ta': 'நெல்/அரிசி',
                'water_need': 'High',
                'suitable_soil': ['Clay', 'Loamy', 'Black', 'Alluvial'],
                'technologies': ['Transplanter', 'Combine Harvester']
            },
            'Sugarcane': {
                'crop_en': 'Sugarcane',
                'crop_ta': 'கரும்பு',
                'water_need': 'High',
                'suitable_soil': ['Loamy', 'Clay', 'Alluvial', 'Black'],
                'technologies': ['Drip', 'Power Weeder']
            },
            'Banana': {
                'crop_en': 'Banana',
                'crop_ta': 'வாழை',
                'water_need': 'High',
                'suitable_soil': ['Alluvial', 'Clay', 'Loamy', 'Red'],
                'technologies': ['Propping', 'Drip']
            },
            'Cotton': {
                'crop_en': 'Cotton',
                'crop_ta': 'பருத்தி',
                'water_need': 'Moderate',
                'suitable_soil': ['Black', 'Loamy', 'Clay', 'Red'],
                'technologies': ['Picker', 'Sprayer']
            },
            'Turmeric': {
                'crop_en': 'Turmeric',
                'crop_ta': 'மஞ்சள்',
                'water_need': 'Moderate',
                'suitable_soil': ['Red', 'Loamy', 'Alluvial', 'Clay', 'Black'],
                'technologies': ['Boiler', 'Polishing Machine']
            },
            'Maize': {
                'crop_en': 'Maize',
                'crop_ta': 'மக்காச்சோளம்',
                'water_need': 'Moderate',
                'suitable_soil': ['Red', 'Loamy', 'Black', 'Sandy'],
                'technologies': ['Sheller', 'Harvester']
            },
            'Chillies': {
                'crop_en': 'Chillies',
                'crop_ta': 'மிளகாய்',
                'water_need': 'Moderate',
                'suitable_soil': ['Black', 'Red', 'Loamy', 'Sandy'],
                'technologies': ['Solar Dryer', 'Drip']
            },
            'Coconut': {
                'crop_en': 'Coconut',
                'crop_ta': 'தென்னை/தேங்காய்',
                'water_need': 'Moderate',
                'suitable_soil': ['Sandy', 'Alluvial', 'Red', 'Loamy'],
                'technologies': ['Tree Climber', 'Drip']
            },
            'Groundnut': {
                'crop_en': 'Groundnut',
                'crop_ta': 'வேர்க்கடலை',
                'water_need': 'Low',
                'suitable_soil': ['Sandy', 'Red', 'Loamy'],
                'technologies': ['Decorticator', 'Digger']
            },
            'Pulses': {
                'crop_en': 'Pulses',
                'crop_ta': 'பயறு வகைகள்',
                'water_need': 'Low',
                'suitable_soil': ['Loamy', 'Red', 'Black', 'Clay', 'Sandy', 'Gravelly', 'Mixed'],
                'technologies': ['Sprinkler', 'Seed Drill']
            },
            'Millets': {
                'crop_en': 'Millets',
                'crop_ta': 'சிறு தானியங்கள்',
                'water_need': 'Low',
                'suitable_soil': ['Red', 'Sandy', 'Laterite', 'Loamy', 'Gravelly', 'Mixed'],
                'technologies': ['Destoner', 'Dehuller']
            },
            'Oilseeds': {
                'crop_en': 'Oilseeds',
                'crop_ta': 'எண்ணெய் வித்துக்கள்',
                'water_need': 'Low',
                'suitable_soil': ['Red', 'Loamy', 'Mixed'],
                'technologies': ['Oil Expeller', 'Rotavator']
            },
            'Tomato': {
                'crop_en': 'Tomato',
                'crop_ta': 'தக்காளி',
                'water_need': 'Moderate',
                'suitable_soil': ['Red', 'Loamy', 'Sandy'],
                'technologies': ['Drip']
            },
            'Watermelon': {
                'crop_en': 'Watermelon',
                'crop_ta': 'தர்பூசணி',
                'water_need': 'Low',
                'suitable_soil': ['Sandy'],
                'technologies': ['Drip']
            }
        }
    
    def get_technology_recommendations(self, farmer_data):
        """Get personalized technology recommendations based on Adoption Category"""
        
        adoption_category = farmer_data.get('adoption_category')
        
        # Fallback
        if not adoption_category: adoption_category = 'Moderate' 

        # Normalize category string
        if 'High' in adoption_category: target_cat = 'High'
        elif 'Moderate' in adoption_category: target_cat = 'Moderate'
        else: target_cat = 'Low'
             
        current_tech = farmer_data.get('technologies_used', [])
        
        # Base recommendations strictly from the category list
        base_tech_names = self.technology_recommendations.get(target_cat, [])
        
        # Filter and Objectify
        recommendations = []
        for tech_name in base_tech_names:
            if tech_name in current_tech: continue
            
            details = self.tech_details.get(tech_name, {})
            recommendations.append({
                'tech_en': details.get('name_en', tech_name),
                'tech_ta': details.get('name_ta', tech_name),
                'description_en': details.get('description_en', ''),
                'description_ta': details.get('description_ta', ''),
                'cost_en': details.get('cost_en', ''),
                'cost_ta': details.get('cost_ta', ''),
                'scheme_en': details.get('subsidy_en', ''),
                'scheme_ta': details.get('subsidy_ta', '')
            })
        
        # --- Context-Aware Additions ---
        land_area = float(farmer_data.get('land_area') or 0)
        water_avail = farmer_data.get('water_availability')
        
        # Example Addition: Basic Drip for Water Scarcity
        if water_avail == 'Scarce' and 'Drip Irrigation' not in current_tech and 'Basic Drip Kit' not in current_tech:
            tech_sugg = 'Basic Drip Kit' if target_cat == 'Low' else 'Drip Irrigation'
            if not any(r['tech_en'] == tech_sugg for r in recommendations):
                details = self.tech_details.get(tech_sugg, {})
                recommendations.insert(0, {
                    'tech_en': details.get('name_en', tech_sugg),
                    'tech_ta': details.get('name_ta', tech_sugg),
                    'description_en': details.get('description_en', ''),
                    'description_ta': details.get('description_ta', ''),
                    'cost_en': details.get('cost_en', ''),
                    'cost_ta': details.get('cost_ta', ''),
                    'scheme_en': details.get('subsidy_en', ''),
                    'scheme_ta': details.get('subsidy_ta', '')
                })
            
        return recommendations[:6]
    
    def get_crop_recommendations(self, farmer_data):
        """Get crop recommendations using ML model or Rule-based fallback"""
        
        if self.has_ml:
            try:
                # Prepare input features
                row = []
                for col in self.feature_order:
                    val = farmer_data.get(col)
                    
                    # Handle land_area separately (float)
                    if col == 'land_area':
                        try:
                            val = float(val or 2.0)
                        except:
                            val = 2.0
                    else:
                        # Categorical encoding
                        if col in self.encoders:
                            le = self.encoders[col]
                            str_val = str(val or "Other")
                            if str_val not in le.classes_:
                                str_val = le.classes_[0]
                            val = le.transform([str_val])[0]
                        else:
                            val = 0
                    row.append(val)
                
                # Predict probabilities
                X_input = pd.DataFrame([row], columns=self.feature_order)
                probs = self.model.predict_proba(X_input)[0]
                
                # Get the encoder for crop labels
                crop_le = self.encoders['crop_recommendation']
                
                # Get indices of top 4 probabilities
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
                
                if len(recommended_crops) >= 4:
                    return recommended_crops[:4]
            except Exception as e:
                print(f"ML Prediction failed: {e}")
                # Fallback to rule-based if ML fails

        # --- Rule-based Fallback (Original Logic) ---
        soil_type = farmer_data.get('soil_type')
        water_availability = farmer_data.get('water_availability')
        
        if not soil_type: return []
        
        water_level = 'Moderate'
        if water_availability in ['Abundant', 'High']: water_level = 'High'
        elif water_availability in ['Scarce', 'Low', '10-12']: water_level = 'Low'
        
        recommended_crops = []
        for crop, details in self.crop_database.items():
            if soil_type not in details['suitable_soil']: continue
            crop_water = details['water_need']
            is_water_suitable = (crop_water == 'Low') or (crop_water == 'Moderate' and water_level != 'Low') or (crop_water == 'High' and water_level == 'High')
            
            if is_water_suitable:
                recommended_crops.append({
                    'crop_en': details['crop_en'],
                    'crop_ta': details['crop_ta'],
                    'reason_en': f"Suitable for {soil_type} and {water_availability or 'available'} water.",
                    'reason_ta': f"{soil_type} மண் மற்றும் {water_availability or 'கிடைக்கக்கூடிய'} நீருக்கு ஏற்றது.",
                    'technologies': details.get('technologies', [])
                })
                
        # Top 4 logic - priority based on user request examples
        irrigation = farmer_data.get('irrigation_source', '')
        priority_crops = []
        if soil_type == 'Red' and irrigation == 'Borewell': priority_crops = ['Groundnut', 'Millets', 'Cotton', 'Tomato']
        elif soil_type == 'Clay' and irrigation == 'Canal': priority_crops = ['Rice', 'Banana', 'Sugarcane', 'Turmeric']
        elif soil_type == 'Sandy': priority_crops = ['Watermelon', 'Groundnut', 'Coconut']
            
        final_crops = []
        for p_crop in priority_crops:
            for r_crop in recommended_crops:
                if r_crop['crop_en'] == p_crop:
                    final_crops.append(r_crop)
                    break
        for r_crop in recommended_crops:
            if r_crop not in final_crops: final_crops.append(r_crop)
                
        return final_crops[:4] if final_crops else self.get_crop_recommendations_generic()

    def get_crop_recommendations_generic(self):
        generic_crops = ['Pulses', 'Millets', 'Tomato', 'Maize']
        recs = []
        for gc in generic_crops:
            details = self.crop_database.get(gc)
            if details:
                recs.append({
                    'crop_en': details['crop_en'],
                    'crop_ta': details['crop_ta'],
                    'reason_en': "Highly resilient crop suitable for various conditions.",
                    'reason_ta': "பல்வேறு நிலைகளுக்கும் ஏற்ற மிகவும் வளமான பயிர்.",
                    'technologies': details.get('technologies', [])
                })
        return recs


    def get_all_recommendations(self, farmer_data):
        return {
            'technologies': self.get_technology_recommendations(farmer_data),
            'crops': self.get_crop_recommendations(farmer_data)
        }

recommendation_engine = RecommendationEngine()
