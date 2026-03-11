from flask import Blueprint, request, jsonify
from ml.predict import predict_behavior
import json

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict-behavior', methods=['POST'])
def predict_behavior_route():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Map frontend form data to model features
        # The frontend keys might be different, so we provide defaults
        
        # Heuristic for technologies
        tech_used = data.get('technologies_used', [])
        if isinstance(tech_used, str):
            try:
                tech_used = json.loads(tech_used)
            except:
                tech_used = []
        
        input_features = {
            'soil_type': data.get('soil_type', 'Alluvial'),
            'land_size': float(data.get('land_area', 2.0) or 2.0),
            'irrigation_source': data.get('irrigation_source', 'Rainfed'),
            'crop_type': data.get('crops', 'Paddy') if isinstance(data.get('crops'), str) else (data.get('crops', ['Paddy'])[0] if data.get('crops') else 'Paddy'),
            'crop_rotation': 'Yes' if data.get('yield_history') else 'No',
            'seasonal_crop': 'Yes' if data.get('water_availability') == 'Monthly' else 'No',
            'irrigation_method': 'Drip' if data.get('tn_micro_irrigation_aware') else 'Manual',
            'irrigation_frequency': 'Daily' if data.get('water_availability') == 'Abundant' else 'Weekly',
            'water_source': data.get('irrigation_source', 'Well'),
            'water_storage': 'Yes' if data.get('borewell_depth') else 'No',
            'access_to_credit': 'Yes' if data.get('has_loan') else 'No',
            'insurance': 'Yes' if data.get('has_insurance') else 'No',
            'subsidy_usage': 'Yes' if any([data.get(k) for k in ['tn_micro_irrigation_aware', 'tn_free_electricity_aware', 'tn_soil_health_aware']]) else 'No',
            'sells_in_uzhavar_santhai': 'Yes' if data.get('selling_uzhavar_sandhai') else 'No',
            'uses_enam': 'Yes' if data.get('using_enam') else 'No',
            'market_distance': 15.0, # Default value
            'drip_irrigation': 'Yes' if 'Drip Irrigation' in tech_used or data.get('tn_micro_irrigation_aware') else 'No',
            'sprinkler_irrigation': 'Yes' if 'Sprinkler' in tech_used else 'No',
            'rainwater_harvesting': 'Yes' if 'Rainwater Harvesting' in tech_used else 'No',
            'soil_moisture_monitoring': 'Yes' if 'Soil Sensors' in tech_used else 'No',
            'attended_training': 'Yes' if data.get('attended_training') else 'No',
            'smartphone_usage': 'Yes' if data.get('using_uzhavan_app') else 'No',
            'agri_apps_usage': 'Yes' if data.get('using_uzhavan_app') else 'No'
        }
        
        # Call the prediction function
        result = predict_behavior(input_features)
        
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
