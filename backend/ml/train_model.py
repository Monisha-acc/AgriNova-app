import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from recommendation import recommendation_engine

def train_model():
    # --- 1. Crop Recommendation Model ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(current_dir, 'dataset.csv')
    df = pd.read_csv(dataset_path)
    
    print("\n--------------------------------------------------")
    print("Starting Crop Recommendation Model Training...\n")
    print(f"Dataset Loaded ({len(df)} records)")
    
    print("\nAdoption Level Categorization Rules:")
    print("- 0 to 40: Low")
    print("- 41 to 70: Medium")
    print("- 71 to 100: High")
    
    print("\nAdoption Level Thresholds:")
    print("  [0-40]   -> Low")
    print("  [41-70]  -> Medium")
    print("  [71-100] -> High")
    
    crop_features = ['soil_type', 'water_availability', 'irrigation_type', 'land_area', 'season']
    print("\nFeatures Used:")
    for feat in crop_features:
        print(f"- {feat}")
        
    categorical_features = ['soil_type', 'water_availability', 'irrigation_type', 'season']
    X_crop = df[crop_features].copy()
    y_crop = df['crop']
    
    crop_encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        X_crop[col] = le.fit_transform(X_crop[col])
        crop_encoders[col] = le
        
    crop_target_encoder = LabelEncoder()
    y_crop_encoded = crop_target_encoder.fit_transform(y_crop)
    
    # Split
    indices = np.arange(len(df))
    train_idx, test_idx = train_test_split(indices, test_size=0.2)
    
    X_train_c = X_crop.iloc[train_idx]
    X_test_c = X_crop.iloc[test_idx]
    y_train_c = y_crop_encoded[train_idx]
    y_test_c = y_crop_encoded[test_idx]
    
    crop_model = RandomForestClassifier(n_estimators=100)
    crop_model.fit(X_train_c, y_train_c)
    crop_acc = accuracy_score(y_test_c, crop_model.predict(X_test_c))
    print(f"\nAccuracy: {crop_acc*100:.1f}%")
    
    # Sample Test for Crop
    idx = test_idx[0]
    print("\nSample Farmer Profile:")
    print(f"   - Soil Type: {df.loc[idx, 'soil_type']}")
    print(f"   - Water: {df.loc[idx, 'water_availability']}")
    print(f"   - Irrigation: {df.loc[idx, 'irrigation_type']}")
    print(f"   - Land: {df.loc[idx, 'land_area']} Acres")
    print(f"   - Season: {df.loc[idx, 'season']}")
    
    crop_probs = crop_model.predict_proba(X_test_c.iloc[0:1])[0]
    top_crop_indices = np.argsort(crop_probs)[-3:][::-1]
    top_crops = crop_target_encoder.inverse_transform(top_crop_indices)
    
    print("\nRecommended Crops (Top 3):")
    for crop in top_crops:
        print(f"   -> {crop}")
    
    joblib.dump(crop_model, os.path.join(current_dir, 'crop_model.pkl'))
    joblib.dump(crop_encoders, os.path.join(current_dir, 'crop_encoders.pkl'))
    joblib.dump(crop_target_encoder, os.path.join(current_dir, 'crop_target_encoder.pkl'))
    print("\nModel Saved: crop_model.pkl")
    print("--------------------------------------------------")

    # --- 2. Adoption Level Model ---
    print("\n--------------------------------------------------")
    print("Starting Adoption Model Training...\n")
    
    adoption_features = ['age', 'education', 'annual_income', 'land_area', 'farming_experience', 'tech_usage_count', 'scheme_awareness', 'risk_tolerance']
    X_adopt = df[adoption_features].copy()
    y_adopt = df['adoption_level']
    
    print("Features Used:")
    for feat in adoption_features:
        print(f"- {feat}")
    
    adopt_categorical = ['education', 'risk_tolerance']
    adopt_encoders = {}
    for col in adopt_categorical:
        le = LabelEncoder()
        X_adopt[col] = le.fit_transform(X_adopt[col])
        adopt_encoders[col] = le
    
    adopt_target_encoder = LabelEncoder()
    y_adopt_encoded = adopt_target_encoder.fit_transform(y_adopt)
    
    X_train_a = X_adopt.iloc[train_idx]
    X_test_a = X_adopt.iloc[test_idx]
    y_train_a = y_adopt_encoded[train_idx]
    y_test_a = y_adopt_encoded[test_idx]
    
    adopt_model = RandomForestClassifier(n_estimators=100)
    adopt_model.fit(X_train_a, y_train_a)
    adopt_acc = accuracy_score(y_test_a, adopt_model.predict(X_test_a))
    print(f"\nAccuracy: {adopt_acc*100:.0f}%")
    
    # Sample Test for Adoption
    print("\nSample Farmer Profile:")
    print(f"   - Age: {df.loc[idx, 'age']}")
    print(f"   - Education: {df.loc[idx, 'education']}")
    print(f"   - Income: ₹{df.loc[idx, 'annual_income']}")
    print(f"   - Experience: {df.loc[idx, 'farming_experience']} Years")
    print(f"   - Tech Usage: {df.loc[idx, 'tech_usage_count']} tools")
    print(f"   - Awareness: {'Yes' if df.loc[idx, 'scheme_awareness'] else 'No'}")
    print(f"   - Risk Tolerance: {df.loc[idx, 'risk_tolerance']}")
    
    adopt_probs = adopt_model.predict_proba(X_test_a.iloc[0:1])[0]
    score = int(max(adopt_probs) * 100)
    
    # Map Level based on Score for terminal display
    if score > 70:
        level = 'High'
    elif score > 40:
        level = 'Medium'
    else:
        level = 'Low'
    
    print("\nAdoption Level (Sample Test):")
    print(f"   -> {level} ({score}%)")
    
    # --- New Tech Recommendation Test ---
    selected_techs = df.loc[idx, 'technologies_used'] if 'technologies_used' in df.columns else []
    # If it's a string from CSV, handle it (though generate_dataset might save it differently)
    if isinstance(selected_techs, str):
        import ast
        try: selected_techs = ast.literal_eval(selected_techs)
        except: selected_techs = []
    
    # We pass the real farmer data to the engine
    farmer_sample = df.loc[idx].to_dict()
    # The engine expects 'adoption_level' to be passed or it uses the data.
    # We already have 'level' from our prediction.
    
    # This will trigger the print statements inside get_technologies
    tech_recs = recommendation_engine.get_technologies(farmer_sample, level)
    
    joblib.dump(adopt_model, os.path.join(current_dir, 'adoption_model.pkl'))
    joblib.dump({'feature_encoders': adopt_encoders, 'target_encoder': adopt_target_encoder}, os.path.join(current_dir, 'adoption_encoder.pkl'))
    print("\nModel Saved: adoption_model.pkl")
    print("--------------------------------------------------")
    
    print("\nFull Model Pipeline Ready!")

if __name__ == "__main__":
    train_model()
