import pandas as pd
import numpy as np
import os

# Define categories
behavior_categories = ['Traditional', 'Transitional', 'Progressive']
soil_types = ['Red', 'Black', 'Alluvial', 'Clay', 'Sandy', 'Loamy', 'Laterite', 'Gravelly', 'Mixed']
irrigation_sources = ['Borewell', 'Canal', 'River', 'Rainfed', 'Farm Pond', 'Other']
crops = ['Rice', 'Sugarcane', 'Banana', 'Cotton', 'Turmeric', 'Maize', 'Chillies', 'Coconut', 'Groundnut', 'Pulses', 'Millets', 'Tomato', 'Watermelon']

def generate_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        # Features
        soil = np.random.choice(soil_types)
        irr_source = np.random.choice(irrigation_sources)
        land_area = np.random.uniform(0.5, 20.0)
        water_availability = np.random.choice(['High', 'Moderate', 'Low'])
        
        # Rule-based behavior for synthetic data
        if land_area > 10 and water_availability == 'High':
            behavior = 'Progressive'
        elif land_area > 3 or water_availability == 'Moderate':
            behavior = 'Transitional'
        else:
            behavior = 'Traditional'
            
        # Target Crop (Logic to make it learnable)
        target_crop = 'Millets' # Default
        if soil == 'Clay' and irr_source == 'Canal':
            target_crop = 'Rice'
        elif soil == 'Black':
            target_crop = 'Cotton'
        elif soil == 'Red' and irr_source == 'Borewell':
            target_crop = 'Groundnut'
        elif soil == 'Sandy':
            target_crop = 'Coconut'
        elif soil == 'Loamy':
            target_crop = 'Banana'
        elif water_availability == 'Low':
            target_crop = 'Pulses'
        else:
            target_crop = np.random.choice(crops)

        data.append({
            'behavior_label': behavior,
            'soil_type': soil,
            'irrigation_source': irr_source,
            'land_area': land_area,
            'water_availability': water_availability,
            'crop_recommendation': target_crop,
            # Add other features to match existing model requirements if needed
            'crop_type': 'Single',
            'crop_rotation': 'Yes',
            'seasonal_crop': 'Yes',
            'irrigation_method': 'Drip' if behavior == 'Progressive' else 'Flood',
            'irrigation_frequency': 'Daily',
            'water_source': irr_source,
            'water_storage': 'Yes',
            'access_to_credit': 'Yes',
            'insurance': 'Yes',
            'subsidy_usage': 'Yes',
            'sells_in_uzhavar_santhai': 'Yes',
            'uses_enam': 'Yes',
            'drip_irrigation': 'Yes',
            'sprinkler_irrigation': 'No',
            'rainwater_harvesting': 'Yes',
            'soil_moisture_monitoring': 'Yes',
            'attended_training': 'Yes',
            'smartphone_usage': 'High',
            'agri_apps_usage': 'Yes'
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_data(1000)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(os.path.join(current_dir, 'dataset.csv'), index=False)
    print(f"Dataset generated with 1000 rows at {os.path.join(current_dir, 'dataset.csv')}")
