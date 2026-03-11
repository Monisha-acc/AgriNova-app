import sqlite3

DATABASE = 'backend/farmer_app.db'

def migrate():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    columns_to_add = [
        ('other_education', 'TEXT'),
        ('other_crops', 'TEXT'),
        ('other_soil_type', 'TEXT'),
        ('other_irrigation_source', 'TEXT'),
        ('other_water_availability', 'TEXT'),
        ('other_yield_history', 'TEXT'),
        ('other_savings_habit', 'TEXT'),
        ('other_risk_level', 'TEXT'),
        ('other_agro_climatic_zone', 'TEXT'),
        ('other_farmer_category', 'TEXT'),
        ('other_market_type', 'TEXT'),
        ('other_scheme', 'TEXT'),
        ('other_gender', 'TEXT'),
        ('other_land_ownership', 'TEXT')
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f'ALTER TABLE farmer_data ADD COLUMN {col_name} {col_type}')
            print(f"Added column {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists")
            else:
                print(f"Error adding column {col_name}: {e}")
    
    conn.commit()
    conn.close()
    print("Migration completed!")

if __name__ == '__main__':
    migrate()
