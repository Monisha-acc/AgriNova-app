import numpy as np
import pandas as pd
import joblib
import os

class AdoptionPredictor:
    def __init__(self):
        # Paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.behavior_model_path = os.path.join(self.current_dir, 'farmer_model.pkl')
        self.crop_model_path = os.path.join(self.current_dir, 'crop_model.pkl')
        self.behavior_encoders_path = os.path.join(self.current_dir, 'encoders.pkl')
        self.crop_encoders_path = os.path.join(self.current_dir, 'crop_encoders.pkl')
        self.crop_target_encoder_path = os.path.join(self.current_dir, 'crop_target_encoder.pkl')
        
        # Load models
        try:
            self.behavior_model = joblib.load(self.behavior_model_path)
            self.crop_model = joblib.load(self.crop_model_path)
            self.behavior_encoders = joblib.load(self.behavior_encoders_path)
            self.crop_encoders = joblib.load(self.crop_encoders_path)
            self.crop_target_encoder = joblib.load(self.crop_target_encoder_path)
            self.is_trained = True
            print("ML Models loaded successfully in prediction.py")
        except Exception as e:
            self.is_trained = False
            print(f"Failed to load ML models: {e}")
            
        self.behavior_features = ['age', 'gender', 'education', 'land_area', 'soil_type', 'irrigation_source', 
                    'water_availability', 'crop_type', 'irrigation_method', 'season', 'technology_usage', 
                    'smartphone_usage', 'attended_training', 'insurance', 'access_to_credit', 
                    'subsidy_usage', 'market_access']

        self.crop_features = ['soil_type', 'water_availability', 'irrigation_type', 'land_area', 'season']

    def _safe_encode(self, col, val, encoders_dict):
        if col not in encoders_dict:
            return val
        le = encoders_dict[col]
        str_val = str(val) if val is not None and str(val).strip() != "" else le.classes_[0]
        if str_val not in le.classes_:
            str_val = le.classes_[0]
        return le.transform([str_val])[0]

    def _safe_float(self, val, default):
        try:
            return float(val) if val is not None and str(val).strip() != "" else default
        except:
            return default

    def _safe_int(self, val, default):
        try:
            return int(val) if val is not None and str(val).strip() != "" else default
        except:
            return default

    def preprocess_input(self, farmer_data):
        # Make a copy of data to not modify the original
        data = {}
        
        # Mapping from DB fields (models.py) to ML fields
        data['age'] = self._safe_int(farmer_data.get('age'), 40)
        data['gender'] = farmer_data.get('gender', 'Male')
        data['education'] = farmer_data.get('education', 'Primary')
        data['land_area'] = self._safe_float(farmer_data.get('land_area'), 2.0)
        data['soil_type'] = farmer_data.get('soil_type', 'Red')
        data['irrigation_source'] = farmer_data.get('irrigation_source') or farmer_data.get('irrig_source') or 'Rainfed'
        data['water_availability'] = farmer_data.get('water_availability') or farmer_data.get('irrig_availability') or 'Medium'
        
        # Derive crop_type from crops list
        crops_list = farmer_data.get('crops', [])
        data['crop_type'] = crops_list[0] if isinstance(crops_list, list) and len(crops_list) > 0 else 'Cash Crop'
        
        # Map irrigation_source/source to method
        data['irrigation_method'] = farmer_data.get('irrig_method') or farmer_data.get('irrigation_source') or 'Rainfed'
        data['season'] = farmer_data.get('season') or 'Kharif'
        
        # Technology usage derivation
        tech_used = farmer_data.get('technologies_used', [])
        if isinstance(tech_used, list):
            tech_count = len(tech_used)
            if tech_count > 3: data['technology_usage'] = 'High'
            elif tech_count > 0: data['technology_usage'] = 'Medium'
            else: data['technology_usage'] = 'Low'
        else:
            data['technology_usage'] = 'Medium'

        # Smartphone usage derivation from digital activity
        digital_activity = (
            farmer_data.get('using_uzhavan_app', 0) or 
            farmer_data.get('watch_agri_youtube', 0) or 
            farmer_data.get('in_whatsapp_groups', 0)
        )
        data['smartphone_usage'] = 'Yes' if digital_activity else 'No'
        
        data['attended_training'] = 'Yes' if farmer_data.get('attended_training') else 'No'
        
        # Insurance & Credit
        data['insurance'] = 'Yes' if farmer_data.get('has_insurance') or farmer_data.get('enrolled_pmfby') else 'No'
        data['access_to_credit'] = 'Yes' if farmer_data.get('has_loan') or farmer_data.get('loan_source') else 'No'
        
        # Subsidies & Market
        data['subsidy_usage'] = 'Yes' if farmer_data.get('amma_two_wheeler_aware') or farmer_data.get('tn_micro_irrigation_aware') else 'No'
        data['market_access'] = 'Yes' if farmer_data.get('selling_uzhavar_sandhai') or farmer_data.get('using_enam') or farmer_data.get('market_linkage') else 'No'
        
        # Encode features
        encoded_data = {}
        # Preprocessing for Behavior Model
        for col in self.behavior_features:
            if col in self.behavior_encoders:
                encoded_data[col] = self._safe_encode(col, data.get(col), self.behavior_encoders)
            else:
                encoded_data[col] = data.get(col)
                
        # Preprocessing for Crop Model
        crop_encoded_data = {}
        for col in self.crop_features:
            if col in self.crop_encoders:
                crop_encoded_data[col] = self._safe_encode(col, data.get(col), self.crop_encoders)
            else:
                crop_encoded_data[col] = data.get(col)

        return pd.DataFrame([encoded_data]), pd.DataFrame([crop_encoded_data])

    def predict(self, farmer_data):
        if not self.is_trained:
            # Fallback
            return self._fallback_predict(farmer_data)
        
        b_input, _ = self.preprocess_input(farmer_data)
        
        # Predict Behavior
        b_pred_enc = self.behavior_model.predict(b_input)[0]
        behavior_label = self.behavior_encoders['behavior_label'].inverse_transform([b_pred_enc])[0]
        
        # Map to Adoption Category
        if 'High' in behavior_label: category = 'High'
        elif 'Medium' in behavior_label: category = 'Medium'
        else: category = 'Low'

        # Score mapping logic
        score_map = {'High': 85, 'Medium': 55, 'Low': 25}
        
        return {
            'adoption_score': score_map.get(category, 50),
            'adoption_category': category,
            'predicted_label': behavior_label
        }

    def predict_crop(self, farmer_data):
        if not self.is_trained:
            return None
        
        _, c_input = self.preprocess_input(farmer_data)
        
        c_pred_enc = self.crop_model.predict(c_input)[0]
        crop_name = self.crop_target_encoder.inverse_transform([c_pred_enc])[0]
        return crop_name

    def _fallback_predict(self, farmer_data):
        return {
            'adoption_score': 50,
            'adoption_category': 'Medium',
            'predicted_label': 'Medium Adoption'
        }

# Global predictor instance
predictor = AdoptionPredictor()
