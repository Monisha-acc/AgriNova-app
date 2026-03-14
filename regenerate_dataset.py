import pandas as pd
import numpy as np
import random

n = 1500

soil_types = ['Red', 'Black', 'Clay', 'Sandy', 'Loamy', 'Alluvial', 'Mixed']
irrigation_methods = ['Drip', 'Sprinkler', 'Flood', 'Rainfed']
water_availabilities = ['High', 'Medium', 'Low']
education_levels = ['None', 'Primary', 'Secondary', 'Higher Secondary', 'Graduate']
genders = ['Male', 'Female']
seasons = ['Kharif', 'Rabi', 'Zaid']
smartphone_usages = ['Yes', 'No']
training_attendances = ['Yes', 'No']
insurances = ['Yes', 'No']
credit_accesses = ['Yes', 'No']
subsidy_usages = ['Yes', 'No']
market_accesses = ['Yes', 'No']
tech_usages = ['Low', 'Medium', 'High']

data = {
    'age': np.random.randint(18, 70, n),
    'gender': np.random.choice(genders, n),
    'education': np.random.choice(education_levels, n),
    'land_area': np.random.uniform(0.5, 20.0, n),
    'soil_type': np.random.choice(soil_types, n),
    'irrigation_source': np.random.choice(['Borewell', 'Canal', 'River', 'Rainfed', 'Farm Pond', 'Other'], n),
    'water_availability': np.random.choice(water_availabilities, n),
    'crop_type': np.random.choice(['Food Crop', 'Cash Crop', 'Horticulture'], n),
    'irrigation_method': np.random.choice(irrigation_methods, n),
    'season': np.random.choice(seasons, n),
    'technology_usage': np.random.choice(tech_usages, n),
    'smartphone_usage': np.random.choice(smartphone_usages, n),
    'attended_training': np.random.choice(training_attendances, n),
    'insurance': np.random.choice(insurances, n),
    'access_to_credit': np.random.choice(credit_accesses, n),
    'subsidy_usage': np.random.choice(subsidy_usages, n),
    'market_access': np.random.choice(market_accesses, n),
}

df = pd.DataFrame(data)

# Stronger rules for Behavior
behavior = []
for i in range(n):
    score = 0
    if df['education'].iloc[i] in ['Graduate', 'Higher Secondary']: score += 2
    if df['technology_usage'].iloc[i] == 'High': score += 3
    elif df['technology_usage'].iloc[i] == 'Medium': score += 1
    if df['smartphone_usage'].iloc[i] == 'Yes': score += 1
    if df['attended_training'].iloc[i] == 'Yes': score += 1
    
    if score >= 5: behavior.append('High Adoption')
    elif score >= 2: behavior.append('Medium Adoption')
    else: behavior.append('Low Adoption')
df['behavior_label'] = behavior

# Strict rules for Crop
crops = []
for i in range(n):
    s = df['soil_type'].iloc[i]
    w = df['water_availability'].iloc[i]
    if w == 'High':
        if s in ['Clay', 'Alluvial']: crops.append('Rice')
        elif s in ['Loamy', 'Black']: crops.append('Sugarcane')
        else: crops.append('Banana')
    elif w == 'Low':
        if s in ['Sandy', 'Red']: crops.append('Groundnut')
        elif s in ['Laterite', 'Gravelly', 'Mixed']: crops.append('Millets')
        else: crops.append('Pulses')
    else: # Medium
        if s in ['Black', 'Loamy']: crops.append('Cotton')
        elif s == 'Red': crops.append('Turmeric')
        elif s == 'Sandy': crops.append('Tomato')
        else: crops.append('Coconut')
df['crop_recommendation'] = crops

df.to_csv('backend/ml/dataset.csv', index=False)
print("dataset.csv generated with shape:", df.shape)

