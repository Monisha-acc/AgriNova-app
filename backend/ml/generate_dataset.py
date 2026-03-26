import pandas as pd
import numpy as np
import os

# --- 1. Master Configurations & Data ---
# These categories must match the drop-down options in the AgriNova frontend forms
soil_types = ['Red', 'Black', 'Clay', 'Sandy', 'Alluvial']
water_availabilities = ['Low', 'Medium', 'High']
irrigation_types = ['Canal', 'Borewell', 'Rainfed', 'Drip', 'Sprinkler']
seasons = ['Kharif', 'Rabi']

# List of all crops supported by the Crop Recommendation model
crops = [
    'Paddy', 'Cotton', 'Groundnut', 'Millets', 'Sugarcane', 
    'Pulses', 'Maize', 'Chillies', 'Banana', 'Turmeric', 'Coconut'
]

def generate_data(num_samples=5000):
    """
    Generates a synthetic dataset of 5,000 farmer profiles to train the AI models.
    This creates realistic relationships between inputs (soil, water) and outputs (crop, adoption).
    """
    data = []
    educations = ['Primary', 'Secondary', 'Graduate']
    risk_tolerances = ['Low', 'Medium', 'High']
    
    # List of modern technologies for the Technology Recommendation engine test
    all_possible_techs = [
        "Drip Irrigation", "Sprinkler Irrigation", "Mulching Sheets", "Greenhouse / Polyhouse", 
        "Soil Testing Kit", "Soil Moisture Sensor", "Weather Forecast Mobile App", 
        "Uzhavan Mobile App", "Farm Mechanization Tools", "Drone Spraying"
    ]
    
    # Start Generation
    for _ in range(num_samples):
        # --- A. Generate Random Farmer Profile Features ---
        soil = np.random.choice(soil_types)
        water = np.random.choice(water_availabilities)
        irrigation = np.random.choice(irrigation_types)
        land_area = round(np.random.uniform(0.5, 20.0), 1) # Standard Farm Size: 0.5 to 20 acres
        season = np.random.choice(seasons)
        
        # --- B. Deterministic Crop Selection Logic (The "Expert" Knowledge) ---
        # This keeps the model accurate by assigning logical crops to soil/water conditions
        if soil == 'Clay' and water == 'High': crop = 'Paddy'
        elif soil == 'Black' and water == 'High': crop = 'Sugarcane'
        elif soil == 'Black' and water == 'Medium': crop = 'Cotton'
        elif soil == 'Black' and water == 'Low': crop = 'Millets'
        elif soil == 'Red' and water == 'High': crop = 'Banana'
        elif soil == 'Red' and water == 'Medium': crop = 'Groundnut'
        elif soil == 'Red' and water == 'Low' and irrigation == 'Borewell': crop = 'Turmeric'
        elif soil == 'Red' and water == 'Low': crop = 'Pulses'
        elif soil == 'Sandy' and water == 'Low': crop = 'Chillies'
        elif soil == 'Sandy' and water == 'Medium': crop = 'Millets'
        elif soil == 'Alluvial' and water == 'High': crop = 'Coconut'
        elif soil == 'Alluvial' and water == 'Medium': crop = 'Maize'
        else:
            # Deterministic Fallback Logic
            if water == 'High': crop = 'Paddy'
            elif water == 'Medium': crop = 'Maize'
            else: crop = 'Millets'

        # --- C. Adoption Model Features (Personal & Digital Profile) ---
        age = np.random.randint(18, 75)
        education = np.random.choice(educations)
        annual_income = np.random.randint(50000, 1000000)
        farming_experience = np.random.randint(1, 50)
        tech_usage_count = np.random.randint(0, 10)
        scheme_awareness = np.random.choice([0, 1])
        risk_tolerance = np.random.choice(risk_tolerances)
        
        # --- D. Adoption Score logic (Rules for 95%+ Prediction Accuracy) ---
        # Scoring weight distribution:
        # Education (35), Income (25), Experience/Usage (30), Risk/Awareness (10)
        score = 0
        if education == 'Graduate': score += 35
        elif education == 'Secondary': score += 15
        
        if annual_income > 600000: score += 25
        elif annual_income > 300000: score += 10
        
        if tech_usage_count > 6: score += 30
        elif tech_usage_count > 3: score += 15
        
        if risk_tolerance == 'High': score += 10
        if scheme_awareness == 1: score += 5
        
        # Minimal noise to help model robustness but keep accuracy high
        score += np.random.randint(-2, 3) 
        score = max(0, min(100, score))
        
        # CATEGORIZATION: Map numerical score to the 3 Adoption Labels
        if score > 70: adoption_level = 'High'
        elif score > 40: adoption_level = 'Medium'
        else: adoption_level = 'Low'

        # --- E. Technologies Selected (Simulation of Current Practice) ---
        # Pick random technologies based on the usage count
        actual_tech_count = min(tech_usage_count, len(all_possible_techs))
        technologies_selected = np.random.choice(all_possible_techs, size=actual_tech_count, replace=False).tolist()

        # Add to Final dataset
        data.append({
            'soil_type': soil,
            'water_availability': water,
            'irrigation_type': irrigation,
            'land_area': land_area,
            'season': season,
            'crop': crop,
            'age': age,
            'education': education,
            'annual_income': annual_income,
            'farming_experience': farming_experience,
            'tech_usage_count': tech_usage_count,
            'scheme_awareness': scheme_awareness,
            'risk_tolerance': risk_tolerance,
            'adoption_level': adoption_level,
            'technologies_used': str(technologies_selected) # Stored as string list for CSV compatibility
        })
    
    return pd.DataFrame(data)

# --- 2. Main Script Execution ---
if __name__ == "__main__":
    print("-" * 50)
    print("AgriNova: Synthetic Dataset Generation Tool")
    print("-" * 50)
    
    # 1. Generate DataFrame with 5,000 samples
    df = generate_data(5000)
    
    # 2. Get absolute path for saving CSV
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'dataset.csv')
    
    # 3. Save CSV
    df.to_csv(file_path, index=False)
    
    # 4. Success Output
    print(f"Dataset Successfully Created with {len(df)} records.")
    print(f"Saved to: {file_path}")
    
    # 5. Display the defined Thresholds for terminal reference
    print("\nAdoption Level Rule Reference:")
    print("  [0-40]   -> Low (Beginner)")
    print("  [41-70]  -> Medium (Intermediate)")
    print("  [71-100] -> High (Advanced)")
    print("-" * 50)
