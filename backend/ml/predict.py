import joblib
import os
import pandas as pd

# Get paths
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'farmer_model.pkl')
encoders_path = os.path.join(current_dir, 'encoders.pkl')

def predict_behavior(input_data):
    """
    Predict farmer behavior based on input features.
    input_data: dict containing feature names and values.
    """
    try:
        # Load model and encoders
        model = joblib.load(model_path)
        encoders = joblib.load(encoders_path)
        
        # Ensure input data is a DataFrame in correct order
        # Columns must match training set (except target)
        feature_order = [
            'soil_type', 'land_size', 'irrigation_source', 'crop_type',
            'crop_rotation', 'seasonal_crop', 'irrigation_method',
            'irrigation_frequency', 'water_source', 'water_storage',
            'access_to_credit', 'insurance', 'subsidy_usage',
            'sells_in_uzhavar_santhai', 'uses_enam', 'market_distance',
            'drip_irrigation', 'sprinkler_irrigation', 'rainwater_harvesting',
            'soil_moisture_monitoring', 'attended_training', 'smartphone_usage',
            'agri_apps_usage'
        ]
        
        # Prepare data
        row = []
        for col in feature_order:
            val = input_data.get(col)
            
            # Encode if it's a categorical column
            if col in encoders and col != 'behavior_label':
                le = encoders[col]
                # If value not in encoder classes, pick a default (first class)
                if str(val) not in le.classes_:
                    val = le.classes_[0]
                val = le.transform([str(val)])[0]
            
            row.append(val)
            
        # Create DF for single prediction
        X_input = pd.DataFrame([row], columns=feature_order)
        
        # Predict
        pred_index = model.predict(X_input)[0]
        
        # Decode target
        target_le = encoders['behavior_label']
        prediction = target_le.inverse_transform([pred_index])[0]
        
        # Get recommendations
        recommendations = {
            "Traditional": {
                "en": "Recommend adopting drip irrigation, attending farmer training programs, and using government schemes.",
                "ta": "சொட்டு நீர் பாசனத்தை மேற்கொள்வது, விவசாயி பயிற்சி திட்டங்களில் பங்கேற்பது மற்றும் அரசு திட்டங்களை பயன்படுத்த பரிந்துரைக்கிறோம்."
            },
            "Transitional": {
                "en": "Recommend improving water management, using eNAM for market access, and adopting digital agriculture tools.",
                "ta": "நீர் நிர்வாகத்தை மேம்படுத்துதல், சந்தை அணுகலுக்கு eNAM ஐப் பயன்படுத்துதல் மற்றும் டிஜிட்டல் விவசாய கருவிகளை ஏற்றுக்கொள்வது என பரிந்துரைக்கிறோம்."
            },
            "Progressive": {
                "en": "Recommend precision farming techniques, IoT based irrigation monitoring, and advanced market integration.",
                "ta": "துல்லியமான விவசாய முறைகள், IoT அடிப்படையிலான பாசன கண்காணிப்பு மற்றும் மேம்பட்ட சந்தை ஒருங்கிணைப்பு ஆகியவற்றை பரிந்துரைக்கிறோம்."
            }
        }
        
        rec = recommendations.get(prediction, recommendations["Traditional"])
        
        return {
            "behavior": prediction,
            "recommendation_en": rec["en"],
            "recommendation_ta": rec["ta"]
        }
    except Exception as e:
        print(f"Prediction error: {e}")
        return {
            "behavior": "Unknown",
            "recommendation_en": "Error occurred during prediction.",
            "recommendation_ta": "கணிப்பின் போது பிழை ஏற்பட்டது."
        }
