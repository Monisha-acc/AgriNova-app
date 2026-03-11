import sqlite3
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'farmer_app.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            password_hash TEXT NOT NULL,
            district TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Farmer data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            
            -- Basic Profile
            age INTEGER,
            gender TEXT,
            education TEXT,
            experience INTEGER,
            income REAL,
            household_size INTEGER,
            
            -- Land & Crop
            land_area REAL,
            land_ownership TEXT,
            crops TEXT,
            soil_type TEXT,
            irrigation_source TEXT,
            water_availability TEXT,
            yield_history TEXT,
            market_linkage TEXT,
            
            -- Technology Usage (JSON array)
            technologies_used TEXT,
            other_technology TEXT,
            
            -- Scheme Awareness (JSON array)
            schemes_aware TEXT,
            other_scheme TEXT,
            
            -- Financial Behaviour
            has_loan INTEGER,
            has_insurance INTEGER,
            savings_habit TEXT,
            risk_level TEXT,
            
            -- Tech Attitude (1-5 scale)
            openness INTEGER,
            trust INTEGER,
            peer_influence INTEGER,
            govt_influence INTEGER,

            -- TN Region Details
            block TEXT,
            taluk TEXT,
            village TEXT,
            agro_climatic_zone TEXT,

            -- Water & Energy
            borewell_depth INTEGER,
            water_scarcity_months INTEGER,
            three_phase_power INTEGER,
            power_hours_per_day INTEGER,

            -- Social & Category
            physically_challenged INTEGER,
            farmer_category TEXT,
            farmer_smart_card INTEGER,

            -- Literacy & Language
            read_tamil INTEGER,
            read_english INTEGER,
            voice_guidance_pref INTEGER,

            -- Market & Training
            selling_uzhavar_sandhai INTEGER,
            using_enam INTEGER,
            market_type TEXT,
            attended_training INTEGER,
            met_vao_aeo INTEGER,
            visited_tnau_farm INTEGER,

            -- Digital Usage
            using_uzhavan_app INTEGER,
            watch_agri_youtube INTEGER,
            in_whatsapp_groups INTEGER,

            -- Specific Scheme Awareness (Flags)
            amma_two_wheeler_aware INTEGER,
            tn_micro_irrigation_aware INTEGER,
            tn_free_electricity_aware INTEGER,
            kalaignar_scheme_aware INTEGER,
            tn_soil_health_aware INTEGER,
            tn_farm_mechanization_aware INTEGER,
            
            -- Other Details (Custom entries)
            other_education TEXT,
            other_crops TEXT,
            other_soil_type TEXT,
            other_irrigation_source TEXT,
            other_water_availability TEXT,
            other_yield_history TEXT,
            other_savings_habit TEXT,
            other_risk_level TEXT,
            other_agro_climatic_zone TEXT,
            other_farmer_category TEXT,
            other_market_type TEXT,
            other_gender TEXT,
            other_land_ownership TEXT,
            
            -- ML Results
            adoption_score REAL,
            adoption_category TEXT,
            segmentation_cluster TEXT,

            -- Extended Financial & Risk Behaviour
            loan_source TEXT,
            repay_on_time INTEGER,
            crop_loss_earlier INTEGER,
            farming_only_income INTEGER,
            other_income_sources INTEGER,
            save_after_harvest INTEGER,
            saving_location TEXT,
            invested_equipment INTEGER,
            digital_payment_usage INTEGER,
            check_market_price INTEGER,
            risk_try_new_methods INTEGER,
            risk_afraid_loss INTEGER,
            risk_follow_neighbors INTEGER,
            enrolled_pmfby INTEGER,
            
            -- Water Irrigation Module
            irrig_method TEXT,
            irrig_source TEXT,
            irrig_availability TEXT,
            irrig_frequency TEXT,
            irrig_drainage TEXT,
            irrig_land_level TEXT,
            irrig_moisture TEXT,
            irrig_crop_age INTEGER,
            irrig_system_cond TEXT,
            irrig_storage TEXT,
            irrig_timing TEXT,
            irrig_rainfall_dep TEXT,
            
            -- Other Water Irrigation Details
            other_irrig_method TEXT,
            other_irrig_source TEXT,
            other_irrig_availability TEXT,
            other_irrig_frequency TEXT,
            other_irrig_drainage TEXT,
            other_irrig_land_level TEXT,
            other_irrig_moisture TEXT,
            other_irrig_system_cond TEXT,
            other_irrig_storage TEXT,
            other_irrig_timing TEXT,
            other_irrig_rainfall_dep TEXT,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

class User:
    @staticmethod
    def create(name, email, phone, password, district):
        """Create new user"""
        conn = get_db()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        
        try:
            cursor.execute('''
                INSERT INTO users (name, email, phone, password_hash, district)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, password_hash, district))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate user"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            return dict(user)
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

class FarmerData:
    @staticmethod
    def create(user_id, data):
        """Create farmer data entry"""
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO farmer_data (
                user_id, age, gender, education, experience, income, household_size,
                land_area, land_ownership, crops, soil_type, irrigation_source,
                water_availability, yield_history, market_linkage,
                technologies_used, other_technology, schemes_aware, other_scheme,
                has_loan, has_insurance, savings_habit, risk_level,
                openness, trust, peer_influence, govt_influence,
                block, taluk, village, agro_climatic_zone,
                borewell_depth, water_scarcity_months, three_phase_power, power_hours_per_day,
                physically_challenged, farmer_category, farmer_smart_card,
                read_tamil, read_english, voice_guidance_pref,
                selling_uzhavar_sandhai, using_enam, market_type,
                attended_training, met_vao_aeo, visited_tnau_farm,
                using_uzhavan_app, watch_agri_youtube, in_whatsapp_groups,
                amma_two_wheeler_aware, tn_micro_irrigation_aware, tn_free_electricity_aware,
                kalaignar_scheme_aware, tn_soil_health_aware, tn_farm_mechanization_aware,
                other_education, other_crops, other_soil_type, other_irrigation_source,
                other_water_availability, other_yield_history, other_savings_habit,
                other_risk_level, other_agro_climatic_zone, other_farmer_category,
                other_market_type, other_gender, other_land_ownership,
                loan_source, repay_on_time, enrolled_pmfby, crop_loss_earlier,
                farming_only_income, other_income_sources, save_after_harvest,
                saving_location, invested_equipment, digital_payment_usage,
                check_market_price, risk_try_new_methods, risk_afraid_loss,
                risk_follow_neighbors,
                irrig_method, irrig_source, irrig_availability, irrig_frequency,
                irrig_drainage, irrig_land_level, irrig_moisture, irrig_crop_age,
                irrig_system_cond, irrig_storage, irrig_timing, irrig_rainfall_dep,
                other_irrig_method, other_irrig_source, other_irrig_availability,
                other_irrig_frequency, other_irrig_drainage, other_irrig_land_level,
                other_irrig_moisture, other_irrig_system_cond, other_irrig_storage,
                other_irrig_timing, other_irrig_rainfall_dep
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data.get('age'),
            data.get('gender'),
            data.get('education'),
            data.get('experience'),
            data.get('income'),
            data.get('household_size'),
            data.get('land_area'),
            data.get('land_ownership'),
            json.dumps(data.get('crops', [])), # Multi-select
            data.get('soil_type'),
            data.get('irrigation_source'),
            data.get('water_availability'),
            data.get('yield_history'),
            data.get('market_linkage'),
            json.dumps(data.get('technologies_used', [])),
            data.get('other_technology'),
            json.dumps(data.get('schemes_aware', [])),
            data.get('other_scheme'),
            data.get('has_loan'),
            data.get('has_insurance'),
            data.get('savings_habit'),
            data.get('risk_level'),
            data.get('openness'),
            data.get('trust'),
            data.get('peer_influence'),
            data.get('govt_influence'),
            # Region Details
            data.get('block'),
            data.get('taluk'),
            data.get('village'),
            data.get('agro_climatic_zone'),
            # Water & Energy
            data.get('borewell_depth'),
            data.get('water_scarcity_months'),
            data.get('three_phase_power'),
            data.get('power_hours_per_day'),
            # Social & Category
            data.get('physically_challenged'),
            data.get('farmer_category'),
            data.get('farmer_smart_card'),
            # Literacy & Language
            data.get('read_tamil'),
            data.get('read_english'),
            data.get('voice_guidance_pref'),
            # Market & Training
            data.get('selling_uzhavar_sandhai'),
            data.get('using_enam'),
            data.get('market_type'),
            data.get('attended_training'),
            data.get('met_vao_aeo'),
            data.get('visited_tnau_farm'),
            # Digital Usage
            data.get('using_uzhavan_app'),
            data.get('watch_agri_youtube'),
            data.get('in_whatsapp_groups'),
            # Scheme Awareness Flags
            data.get('amma_two_wheeler_aware'),
            data.get('tn_micro_irrigation_aware'),
            data.get('tn_free_electricity_aware'),
            data.get('kalaignar_scheme_aware'),
            data.get('tn_soil_health_aware'),
            data.get('tn_farm_mechanization_aware'),
            data.get('other_education'),
            data.get('other_crops'),
            data.get('other_soil_type'),
            data.get('other_irrigation_source'),
            data.get('other_water_availability'),
            data.get('other_yield_history'),
            data.get('other_savings_habit'),
            data.get('other_risk_level'),
            data.get('other_agro_climatic_zone'),
            data.get('other_farmer_category'),
            data.get('other_market_type'),
            data.get('other_gender'),
            data.get('other_land_ownership'),
            data.get('loan_source'),
            data.get('repay_on_time'),
            data.get('enrolled_pmfby'),
            data.get('crop_loss_earlier'),
            data.get('farming_only_income'),
            data.get('has_other_income'),
            data.get('save_after_harvest'),
            data.get('saving_location'),
            data.get('invested_equipment'),
            data.get('digital_payment_usage'),
            data.get('check_market_price'),
            data.get('risk_try_new_methods'),
            data.get('risk_afraid_loss'),
            data.get('risk_follow_neighbors'),
            data.get('irrig_method'),
            data.get('irrig_source'),
            data.get('irrig_availability'),
            data.get('irrig_frequency'),
            data.get('irrig_drainage'),
            data.get('irrig_land_level'),
            data.get('irrig_moisture'),
            data.get('irrig_crop_age'),
            data.get('irrig_system_cond'),
            data.get('irrig_storage'),
            data.get('irrig_timing'),
            data.get('irrig_rainfall_dep'),
            data.get('other_irrig_method'),
            data.get('other_irrig_source'),
            data.get('other_irrig_availability'),
            data.get('other_irrig_frequency'),
            data.get('other_irrig_drainage'),
            data.get('other_irrig_land_level'),
            data.get('other_irrig_moisture'),
            data.get('other_irrig_system_cond'),
            data.get('other_irrig_storage'),
            data.get('other_irrig_timing'),
            data.get('other_irrig_rainfall_dep')
        ))
        
        conn.commit()
        farmer_id = cursor.lastrowid
        conn.close()
        return farmer_id
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get farmer data by user ID"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM farmer_data WHERE user_id = ? ORDER BY created_at DESC LIMIT 1', (user_id,))
        data = cursor.fetchone()
        conn.close()
        
        if data:
            result = dict(data)
            # Parse JSON fields
            result['technologies_used'] = json.loads(result['technologies_used']) if result['technologies_used'] else []
            result['schemes_aware'] = json.loads(result['schemes_aware']) if result['schemes_aware'] else []
            result['crops'] = json.loads(result['crops']) if (result.get('crops') and result['crops'].startswith('[')) else [result['crops']] if result.get('crops') else []
            return result
        return None
    
    @staticmethod
    def update_ml_results(farmer_id, adoption_score, adoption_category, segmentation_cluster):
        """Update ML prediction results"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE farmer_data 
            SET adoption_score = ?, adoption_category = ?, segmentation_cluster = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (adoption_score, adoption_category, segmentation_cluster, farmer_id))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    init_db()
