import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
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

# Ensure required categorical columns are strings
categorical_cols = [
    'gender', 'education', 'soil_type', 'irrigation_source', 'water_availability',
    'crop_type', 'irrigation_method', 'season', 'technology_usage', 'smartphone_usage',
    'attended_training', 'insurance', 'access_to_credit', 'subsidy_usage', 'market_access'
]

# Ensure targets are strings
target_cols = ['behavior_label', 'crop_recommendation']

encoders = {}
for col in categorical_cols + target_cols:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

# Dictionary to store encoders
joblib.dump(encoders, encoders_path)

# --- Train Behavior Model ---
behavior_features = ['age', 'gender', 'education', 'land_area', 'soil_type', 'irrigation_source', 
                    'water_availability', 'crop_type', 'irrigation_method', 'season', 'technology_usage', 
                    'smartphone_usage', 'attended_training', 'insurance', 'access_to_credit', 
                    'subsidy_usage', 'market_access']

X_behavior = df[behavior_features]
y_behavior = df['behavior_label']

X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X_behavior, y_behavior, test_size=0.2, random_state=42)

behavior_model = RandomForestClassifier(n_estimators=200, max_depth=12, min_samples_split=5, random_state=42)
behavior_model.fit(X_train_b, y_train_b)

b_pred = behavior_model.predict(X_test_b)
b_acc = accuracy_score(y_test_b, b_pred)

print(f"Behavior Model Accuracy: {b_acc:.2f}")
print("Behavior Model Classification Report:")
print(classification_report(y_test_b, b_pred, target_names=encoders['behavior_label'].classes_))

# Save behavior model
joblib.dump(behavior_model, behavior_model_path)

# --- Train Crop Recommendation Model ---
# Specified features: Soil type, Water availability, Irrigation method, Season, Land area, Previous crop
crop_features = ['soil_type', 'water_availability', 'irrigation_method', 'season', 'land_area', 'crop_type']

X_crop = df[crop_features]
y_crop = df['crop_recommendation']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_crop, y_crop, test_size=0.2, random_state=42)

crop_model = RandomForestClassifier(n_estimators=200, max_depth=12, min_samples_split=5, random_state=42)
crop_model.fit(X_train_c, y_train_c)

c_pred = crop_model.predict(X_test_c)
c_acc = accuracy_score(y_test_c, c_pred)

print(f"Crop Model Accuracy: {c_acc:.2f}")
print("Crop Model Classification Report:")
print(classification_report(y_test_c, c_pred, target_names=encoders['crop_recommendation'].classes_, zero_division=0))

# Save crop model
joblib.dump(crop_model, crop_model_path)

print(f"\nModels and Encoders saved in {current_dir}")
