from flask import Blueprint, request, jsonify, session
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new farmer"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        district = data.get('district')
        
        # Handle empty strings for optional fields
        if email == '': email = None
        if phone == '': phone = None
        
        # Validation
        if not all([name, password, district]):
            return jsonify({'error': 'Name, password, and district are required'}), 400
        
        if not email and not phone:
            return jsonify({'error': 'Either email or phone is required'}), 400
        
        # Create user
        user_id = User.create(name, email, phone, password, district)
        
        if user_id is None:
            return jsonify({'error': 'Email already exists'}), 400
        
        # Set session
        session['user_id'] = user_id
        session['user_name'] = name
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': user_id,
            'name': name,
            'district': district
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login farmer"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate
        user = User.authenticate(email, password)
        
        if user is None:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Set session
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user['id'],
            'name': user['name'],
            'district': user['district']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout farmer"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        if user:
            return jsonify({
                'logged_in': True,
                'user_id': user['id'],
                'name': user['name'],
                'district': user['district']
            }), 200
    
    return jsonify({'logged_in': False}), 200
