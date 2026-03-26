import numpy as np
import joblib
import pandas as pd
import os

class RecommendationEngine:
    def __init__(self):
        # Paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.crop_model_path = os.path.join(self.current_dir, 'crop_model.pkl')
        self.crop_encoders_path = os.path.join(self.current_dir, 'crop_encoders.pkl')
        self.crop_target_encoder_path = os.path.join(self.current_dir, 'crop_target_encoder.pkl')
        
        self.adopt_model_path = os.path.join(self.current_dir, 'adoption_model.pkl')
        self.adopt_encoder_path = os.path.join(self.current_dir, 'adoption_encoder.pkl')
        
        # Load Crop Model
        try:
            self.crop_model = joblib.load(self.crop_model_path)
            self.crop_encoders = joblib.load(self.crop_encoders_path)
            self.crop_target_encoder = joblib.load(self.crop_target_encoder_path)
            self.has_crop_ml = True
            print("🌾 Crop Recommendation model loaded.")
        except Exception as e:
            self.has_crop_ml = False
            print(f"❌ Crop model failed: {e}")
            
        # Load Adoption Model
        try:
            self.adopt_model = joblib.load(self.adopt_model_path)
            adopt_data = joblib.load(self.adopt_encoder_path)
            self.adopt_feature_encoders = adopt_data['feature_encoders']
            self.adopt_target_encoder = adopt_data['target_encoder']
            self.has_adopt_ml = True
            print("🤖 Adoption Prediction model loaded.")
        except Exception as e:
            self.has_adopt_ml = False
            print(f"❌ Adoption model failed: {e}")
            
    def get_top_3_crops(self, farmer_data):
        if not self.has_crop_ml:
            return ["Paddy", "Millets", "Groundnut"]
            
        try:
            # Map inputs strictly (only these 5)
            # soil_type, water_availability, irrigation_type, land_area, season
            
            # Map backend database field names to ML requirement names
            soil_type = farmer_data.get('soil_type', 'Red')
            water_availability = farmer_data.get('water_availability', 'Medium')
            # Handle mapping 'irrigation_source' or 'irrig_method' to 'irrigation_type'
            irrigation_type = farmer_data.get('irrigation_type') or farmer_data.get('irrigation_source') or 'Canal'
            # The dropdown for irrigation_type in FarmerForm has 'Rainfed', 'Borewell', 'Canal', 'Drip', 'Sprinkler'
            # Normalizing it to match generate_dataset categories
            if irrigation_type not in ['Canal', 'Borewell', 'Rainfed', 'Drip', 'Sprinkler']:
                irrigation_type = 'Canal' # Fallback to common type
                
            land_area = float(farmer_data.get('land_area', 2.0) or 2.0)
            season = farmer_data.get('season', 'Kharif')
            
            # Prepare input data
            input_dict = {
                'soil_type': soil_type,
                'water_availability': water_availability,
                'irrigation_type': irrigation_type,
                'land_area': land_area,
                'season': season
            }
            
            X_input = pd.DataFrame([input_dict])
            
            # Encode categorical features
            for col, le in self.crop_encoders.items():
                if input_dict[col] not in le.classes_:
                    input_dict[col] = le.classes_[0]
                X_input[col] = le.transform([input_dict[col]])
                
            # Predict Probabilities
            probs = self.crop_model.predict_proba(X_input)[0]
            
            # Get Top 3
            top_indices = np.argsort(probs)[-3:][::-1]
            top_crops = self.crop_target_encoder.inverse_transform(top_indices)
            
            return list(top_crops)
            
        except Exception as e:
            print(f"Crop prediction error: {e}")
            return ["Paddy", "Millets", "Groundnut"]

    def get_adoption_level(self, farmer_data):
        if not self.has_adopt_ml:
            return "Medium", 50
            
        try:
            # age, education, annual_income, land_area, farming_experience, tech_usage_count, scheme_awareness, risk_tolerance
            input_dict = {
                'age': int(farmer_data.get('age', 40)),
                'education': farmer_data.get('education', 'Secondary'),
                'annual_income': float(farmer_data.get('annual_income', 300000)),
                'land_area': float(farmer_data.get('land_area', 2.0)),
                'farming_experience': int(farmer_data.get('experience', 10)),
                'tech_usage_count': int(len(farmer_data.get('technologies_used', []))),
                'scheme_awareness': 1 if len(farmer_data.get('schemes_aware', [])) > 0 else 0,
                'risk_tolerance': farmer_data.get('risk_tolerance', 'Medium')
            }
            
            X_input = pd.DataFrame([input_dict])
            for col, le in self.adopt_feature_encoders.items():
                if input_dict[col] not in le.classes_:
                    input_dict[col] = le.classes_[0]
                X_input[col] = le.transform([input_dict[col]])
                
            probs = self.adopt_model.predict_proba(X_input)[0]
            score = int(max(probs) * 100)
            
            # Map Level based on Score as requested by user
            if score > 70:
                level = 'High'
            elif score > 40:
                level = 'Medium'
            else:
                level = 'Low'
            
            return level, score
        except Exception as e:
            print(f"Adoption prediction error: {e}")
            return "Medium", 50

    def get_technologies(self, farmer_data, adoption_level):
        """
        New Technology Recommendation Engine based on Adoption Level and Filtering
        """
        # 1. Master Technology List with Metadata
        TECH_MASTER = {
            "Soil Testing Kit": {
                "tech_en": "Soil Testing Kit", "tech_ta": "மண் பரிசோதனை கிட்",
                "description_en": "Helps analyze nutrient levels to optimize fertilizer use.",
                "description_ta": "உரப் பயன்பாட்டை மேம்படுத்த ஊட்டச்சத்து அளவை பகுப்பாய்வு செய்ய உதவுகிறது.",
                "cost_en": "Low", "cost_ta": "குறைவு",
                "scheme_en": "Soil Health Card Scheme", "scheme_ta": "மண் சுகாதார அட்டை திட்டம்"
            },
            "Weather Forecast Mobile App": {
                "tech_en": "Weather Forecast Mobile App", "tech_ta": "வானிலை முன்னறிவிப்பு செயலி",
                "description_en": "Receive real-time weather alerts and rain predictions.",
                "description_ta": "உண்மையான நேரத்தில் வானிலை எச்சரிக்கைகள் மற்றும் மழை கணிப்புகளைப் பெறுங்கள்.",
                "cost_en": "Low", "cost_ta": "இலவசம்/குறைவு",
                "scheme_en": "Digital Agriculture Mission", "scheme_ta": "டிஜிட்டல் வேளாண்மை இயக்கம்"
            },
            "Uzhavan Mobile App": {
                "tech_en": "Uzhavan Mobile App", "tech_ta": "உழவன் மொபைல் செயலி",
                "description_en": "Official TN Govt app for market prices and subsidies.",
                "description_ta": "சந்தை விலைகள் மற்றும் மானியங்களுக்கான அதிகாரப்பூர்வ தமிழக அரசு செயலி.",
                "cost_en": "Low", "cost_ta": "இலவசம்",
                "scheme_en": "TNAU Digital Extension", "scheme_ta": "TNAU டிஜிட்டல் விரிவாக்கம்"
            },
            "Mulching Sheets": {
                "tech_en": "Mulching Sheets", "tech_ta": "மல்சிங் தாள்கள்",
                "description_en": "Conserves soil moisture and prevents weed growth.",
                "description_ta": "மண் ஈரப்பதத்தைப் பாதுகாக்கிறது மற்றும் களை வளர்ச்சியைத் தடுக்கிறது.",
                "cost_en": "Medium", "cost_ta": "நடுத்தரம்",
                "scheme_en": "Horticulture Development Scheme", "scheme_ta": "தோட்டக்கலை மேம்பாட்டுத் திட்டம்"
            },
            "Drip Irrigation": {
                "tech_en": "Drip Irrigation", "tech_ta": "சொட்டு நீர் பாசனம்",
                "description_en": "Precision water delivery to plant roots.",
                "description_ta": "செடியின் வேர்களுக்குத் துல்லியமாகத் தண்ணீர் வழங்குகிறது.",
                "cost_en": "High", "cost_ta": "அதிகம்",
                "scheme_en": "PMKSY (Micro-Irrigation)", "scheme_ta": "மைக்ரோ பாசனத் திட்டம் (PMKSY)"
            },
            "Sprinkler Irrigation": {
                "tech_en": "Sprinkler Irrigation", "tech_ta": "தெளிப்பு நீர் பாசனம்",
                "description_en": "Provides rain-like irrigation for field crops.",
                "description_ta": "வயல் பயிர்களுக்கு மலை போன்ற பாசனத்தை வழங்குகிறது.",
                "cost_en": "Medium", "cost_ta": "நடுத்தரம்",
                "scheme_en": "National Mission on Sustainable Agriculture", "scheme_ta": "நிலையான வேளாண்மைக்கான தேசிய இயக்கம்"
            },
            "Farm Mechanization Tools": {
                "tech_en": "Farm Mechanization Tools", "tech_ta": "விவசாய கருவிகள்",
                "description_en": "Modern machinery like power tillers for efficient labor.",
                "description_ta": "திறமையான உழைப்பிற்காக பவர் டில்லர் போன்ற நவீன இயந்திரங்கள்.",
                "cost_en": "High", "cost_ta": "அதிகம்",
                "scheme_en": "Agricultural Mechanization Mission", "scheme_ta": "விவசாய இயந்திரமயமாக்கல் இயக்கம்"
            },
            "Soil Moisture Sensor": {
                "tech_en": "Soil Moisture Sensor", "tech_ta": "மண் ஈரப்பதம் சென்சார்",
                "description_en": "Monitors soil water levels via smartphone.",
                "description_ta": "ஸ்மார்ட்போன் மூலம் மண் நீர்மட்டத்தைக் கண்காணிக்கிறது.",
                "cost_en": "Medium", "cost_ta": "நடுத்தரம்",
                "scheme_en": "Precision Farming Scheme", "scheme_ta": "துல்லியப் பண்ணையத் திட்டம்"
            },
            "Greenhouse / Polyhouse": {
                "tech_en": "Greenhouse / Polyhouse", "tech_ta": "பசுமை இல்லம்",
                "description_en": "Controlled environment for high-value crops.",
                "description_ta": "உயர்மதிப்புப் பயிர்களுக்கான கட்டுப்படுத்தப்பட்ட சூழல்.",
                "cost_en": "High", "cost_ta": "அதிகம்",
                "scheme_en": "National Horticulture Board", "scheme_ta": "தேசிய தோட்டக்கலை வாரியம்"
            },
            "Drone Spraying": {
                "tech_en": "Drone Spraying", "tech_ta": "ட்ரோன் தெளித்தல்",
                "description_en": "Automated pesticide spraying using drones.",
                "description_ta": "ட்ரோன்களைப் பயன்படுத்தித் தானியங்கி பூச்சிக்கொல்லி தெளித்தல்.",
                "cost_en": "High", "cost_ta": "அதிகம்",
                "scheme_en": "SMAM (Sub-Mission on Agri Mechanization)", "scheme_ta": "SMAM (வேளாண் இயந்திரமயமாக்கல் துணைத் திட்டம்)"
            }
        }

        # 2. Logic: Baseline Assignment
        baseline_map = {
            "Low": ["Soil Testing Kit", "Weather Forecast Mobile App", "Uzhavan Mobile App", "Mulching Sheets"],
            "Medium": ["Drip Irrigation", "Sprinkler Irrigation", "Farm Mechanization Tools", "Soil Moisture Sensor"],
            "High": ["Greenhouse / Polyhouse", "Drone Spraying", "Soil Moisture Sensor", "Farm Mechanization Tools"]
        }
        
        base_list = baseline_map.get(adoption_level, baseline_map["Low"])
        
        # 3. Filter Already Selected Tech
        user_selected = farmer_data.get('technologies_used', [])
        # Normalizing names for comparison
        recommended_keys = [tech for tech in base_list if tech not in user_selected]
        
        # 4. Minimum 4 Results Ensure
        if len(recommended_keys) < 4:
            # Flatten all other categories for fallback
            all_other_techs = ["Soil Testing Kit", "Weather Forecast Mobile App", "Uzhavan Mobile App", "Mulching Sheets", 
                                "Drip Irrigation", "Sprinkler Irrigation", "Farm Mechanization Tools", "Soil Moisture Sensor", 
                                "Greenhouse / Polyhouse", "Drone Spraying"]
            
            for tech in all_other_techs:
                if len(recommended_keys) >= 4:
                    break
                if tech not in recommended_keys and tech not in user_selected:
                    recommended_keys.append(tech)
        
        # Final formatting
        tech_results = [TECH_MASTER[key] for key in recommended_keys[:4]] # type: ignore
        
        return tech_results

    def get_all_recommendations(self, farmer_data):
        top_crops = self.get_top_3_crops(farmer_data)
        level, score = self.get_adoption_level(farmer_data)
        
        # Fetch technologies using the new logic
        technologies = self.get_technologies(farmer_data, level)
        
        return {
            "recommended_crops": top_crops,
            "adoption_level": level,
            "adoption_score": score,
            "technologies": technologies,
            "crops": [
                {"crop_en": crop, "crop_ta": self._get_tamil_name(crop)} 
                for crop in top_crops
            ]
        }

    def _get_tamil_name(self, crop_en):
        names = {
            'Paddy': 'நெல்',
            'Cotton': 'பருத்தி',
            'Groundnut': 'நிலக்ககடலை',
            'Millets': 'சிறு தானியங்கள்',
            'Sugarcane': 'கரும்பு',
            'Pulses': 'பயறு வகைகள்',
            'Maize': 'சோளம்',
            'Chillies': 'மிளகாய்',
            'Banana': 'வாழை',
            'Turmeric': 'மஞ்சள்',
            'Coconut': 'தேங்காய்'
        }
        return names.get(crop_en, crop_en)

recommendation_engine = RecommendationEngine()
