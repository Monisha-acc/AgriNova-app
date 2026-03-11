import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os

class AdoptionPredictor:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.lr_model = LogisticRegression(random_state=42, max_iter=1000)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(self, farmer_data):
        """Convert farmer data to feature vector"""
        features = []
        
        # Helper function to safely get numeric value
        def safe_int(value, default):
            if value is None:
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        
        def safe_float(value, default):
            if value is None:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        # Age
        features.append(safe_int(farmer_data.get('age'), 40))
        
        # Education (encoded)
        education_map = {'None': 0, 'Primary': 1, 'Secondary': 2, 'Higher Secondary': 3, 'Graduate': 4}
        features.append(education_map.get(farmer_data.get('education', 'Primary'), 1))
        
        # Experience
        features.append(safe_int(farmer_data.get('experience'), 10))
        
        # Income (in lakhs)
        features.append(safe_float(farmer_data.get('income'), 100000) / 100000)
        
        # Household size
        features.append(safe_int(farmer_data.get('household_size'), 4))
        
        # Land area
        features.append(safe_float(farmer_data.get('land_area'), 2))
        
        # Land ownership (1 for owned, 0 for rented)
        features.append(1 if farmer_data.get('land_ownership') == 'Owned' else 0)
        
        # Water availability (encoded)
        water_map = {'Scarce': 0, 'Moderate': 1, 'Abundant': 2}
        features.append(water_map.get(farmer_data.get('water_availability', 'Moderate'), 1))
        
        # Market linkage (1 for yes, 0 for no)
        features.append(1 if farmer_data.get('market_linkage') == 'Yes' else 0)
        
        # Number of technologies used
        tech_used = farmer_data.get('technologies_used', [])
        features.append(len(tech_used) if tech_used else 0)
        
        # Number of schemes aware
        schemes_aware = farmer_data.get('schemes_aware', [])
        features.append(len(schemes_aware) if schemes_aware else 0)
        
        # Financial behaviour
        features.append(1 if farmer_data.get('has_loan') else 0)
        features.append(1 if farmer_data.get('has_insurance') else 0)
        
        # Savings habit (encoded)
        savings_map = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Regularly': 3}
        features.append(savings_map.get(farmer_data.get('savings_habit', 'Sometimes'), 2))
        
        # Risk level (encoded)
        risk_map = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}
        features.append(risk_map.get(farmer_data.get('risk_level', 'Moderate'), 2))
        
        # Tech attitude scores (1-5)
        features.append(safe_int(farmer_data.get('openness'), 3))
        features.append(safe_int(farmer_data.get('trust'), 3))
        features.append(safe_int(farmer_data.get('peer_influence'), 3))
        features.append(safe_int(farmer_data.get('govt_influence'), 3))
        
        return np.array(features).reshape(1, -1)
    
    def train(self, X, y):
        """Train both models"""
        X_scaled = self.scaler.fit_transform(X)
        self.rf_model.fit(X_scaled, y)
        self.lr_model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, farmer_data):
        """Predict adoption behavior"""
        if not self.is_trained:
            # Use deterministic rule-based weighted scoring
            return self._calculate_adoption_score(farmer_data)
        
        features = self.prepare_features(farmer_data)
        features_scaled = self.scaler.transform(features)
        
        # Get predictions from both models
        rf_prob = self.rf_model.predict_proba(features_scaled)[0][1]
        lr_prob = self.lr_model.predict_proba(features_scaled)[0][1]
        
        # Average the probabilities
        adoption_score = (rf_prob + lr_prob) / 2 * 100
        
        # Categorize
        if adoption_score >= 75:
            category = 'High'
        elif adoption_score >= 40:
            category = 'Moderate'
        else:
            category = 'Low'
        
        return {
            'adoption_score': round(adoption_score, 2),
            'adoption_category': category,
            'rf_probability': round(rf_prob * 100, 2),
            'lr_probability': round(lr_prob * 100, 2)
        }
    
    def _calculate_adoption_score(self, farmer_data):
        """
        Calculate adoption score (0-100) based on weighted features.
        This is a deterministic logic for cold-start (no trained model).
        """
        score = 0
        
        # 1. Demographics (Max 25)
        # Age: Younger farmers (<35) tend to adopt faster
        age = int(farmer_data.get('age') or 40)
        if age < 35: score += 10
        elif age <= 50: score += 5
        
        # Education: Higher education correlates with adoption
        edu = farmer_data.get('education', 'Primary')
        edu_scores = {'Graduate': 15, 'Higher Secondary': 10, 'Secondary': 5, 'Primary': 2, 'None': 0}
        score += edu_scores.get(edu, 2)
        
        # 2. Assets (Max 20)
        # Land Size
        land = float(farmer_data.get('land_area') or 2)
        if land > 5: score += 10
        elif land >= 2: score += 5
        
        # Water
        water = farmer_data.get('water_availability', 'Moderate')
        if water == 'Abundant': score += 10
        elif water == 'Moderate': score += 5
        
        # 3. Behavior & Awareness (Max 30)
        # Tech Usage: +5 per tech (max 15)
        tech_count = len(farmer_data.get('technologies_used', []))
        score += min(tech_count * 5, 15)
        
        # Scheme Awareness: +3 per scheme (max 9)
        scheme_count = len(farmer_data.get('schemes_aware', []))
        score += min(scheme_count * 3, 9)
        
        # Digital Engagement
        if farmer_data.get('using_uzhavan_app'): score += 6
        
        # 4. Financial (Max 15)
        if farmer_data.get('has_insurance'): score += 5
        if farmer_data.get('has_loan'): score += 5 # Access to credit
        
        savings = farmer_data.get('savings_habit', 'Sometimes')
        if savings == 'Regularly': score += 5
        
        # 5. Attitude (Max 10)
        # Openness to new ideas (1-5)
        openness = int(farmer_data.get('openness') or 3)
        score += openness * 2 # Max 10
        
        # --- Bonus/Penalty ---
        # Region Bonus
        zone = farmer_data.get('agro_climatic_zone')
        if zone in ['Delta', 'Cauvery Delta']: score += 5
        
        # Clamp Score
        score = max(0, min(100, score))
        
        # Strict Categorization
        if score >= 75:
            category = 'High'
        elif score >= 40:
            category = 'Moderate'
        else:
            category = 'Low'
            
        return {
            'adoption_score': round(score, 2),
            'adoption_category': category,
            'rf_probability': 0, # Placeholder
            'lr_probability': 0  # Placeholder
        }
    
    def save_models(self, path='models'):
        """Save trained models"""
        if not os.path.exists(path):
            os.makedirs(path)
        joblib.dump(self.rf_model, f'{path}/rf_model.pkl')
        joblib.dump(self.lr_model, f'{path}/lr_model.pkl')
        joblib.dump(self.scaler, f'{path}/scaler.pkl')
    
    def load_models(self, path='models'):
        """Load trained models"""
        try:
            self.rf_model = joblib.load(f'{path}/rf_model.pkl')
            self.lr_model = joblib.load(f'{path}/lr_model.pkl')
            self.scaler = joblib.load(f'{path}/scaler.pkl')
            self.is_trained = True
            return True
        except:
            return False

# Global predictor instance
predictor = AdoptionPredictor()
