import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Get paths
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, 'dataset.csv')
behavior_model_path = os.path.join(current_dir, 'farmer_model.pkl')
crop_model_path = os.path.join(current_dir, 'crop_model.pkl')
encoders_path = os.path.join(current_dir, 'encoders.pkl')

# Load dataset
df = pd.read_csv(dataset_path)

# Categorical columns to encode
categorical_cols = [
    'soil_type', 'irrigation_source', 'crop_type', 'crop_rotation', 
    'seasonal_crop', 'irrigation_method', 'irrigation_frequency', 
    'water_source', 'water_storage', 'access_to_credit', 'insurance', 
    'subsidy_usage', 'sells_in_uzhavar_santhai', 'uses_enam', 
    'drip_irrigation', 'sprinkler_irrigation', 'rainwater_harvesting', 
    'soil_moisture_monitoring', 'attended_training', 'smartphone_usage', 
    'agri_apps_usage', 'water_availability'
]

# Target columns
target_cols = ['behavior_label', 'crop_recommendation']

# Dictionary to store encoders
encoders = {}

# Encode categorical features
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# Encode targets
for col in target_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# Prepare Features
X = df.drop(target_cols, axis=1)

# --- Train Behavior Model ---
y_behavior = df['behavior_label']
X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X, y_behavior, test_size=0.2, random_state=42)
behavior_model = RandomForestClassifier(n_estimators=100, random_state=42)
behavior_model.fit(X_train_b, y_train_b)
b_acc = accuracy_score(y_test_b, behavior_model.predict(X_test_b))

# --- Train Crop Model ---
y_crop = df['crop_recommendation']
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_crop, test_size=0.2, random_state=42)
crop_model = RandomForestClassifier(n_estimators=100, random_state=42)
crop_model.fit(X_train_c, y_train_c)
c_acc = accuracy_score(y_test_c, crop_model.predict(X_test_c))

# Save models and encoders
joblib.dump(behavior_model, behavior_model_path)
joblib.dump(crop_model, crop_model_path)
joblib.dump(encoders, encoders_path)

print(f"Behavior Model Accuracy: {b_acc:.2f}")
print(f"Crop Model Accuracy: {c_acc:.2f}")
print(f"Models and Encoders saved in {current_dir}")
