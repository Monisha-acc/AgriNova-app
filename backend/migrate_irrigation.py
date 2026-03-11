import sqlite3

DATABASE = '/home/infant/Downloads/AgriNova-main-main/backend/farmer_app.db'

def migrate():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    new_columns = [
        ("irrig_method", "TEXT"),
        ("irrig_source", "TEXT"),
        ("irrig_availability", "TEXT"),
        ("irrig_frequency", "TEXT"),
        ("irrig_drainage", "TEXT"),
        ("irrig_land_level", "TEXT"),
        ("irrig_moisture", "TEXT"),
        ("irrig_crop_age", "INTEGER"),
        ("irrig_system_cond", "TEXT"),
        ("irrig_storage", "TEXT"),
        ("irrig_timing", "TEXT"),
        ("irrig_rainfall_dep", "TEXT"),
        ("other_irrig_method", "TEXT"),
        ("other_irrig_source", "TEXT"),
        ("other_irrig_availability", "TEXT"),
        ("other_irrig_frequency", "TEXT"),
        ("other_irrig_drainage", "TEXT"),
        ("other_irrig_land_level", "TEXT"),
        ("other_irrig_moisture", "TEXT"),
        ("other_irrig_system_cond", "TEXT"),
        ("other_irrig_storage", "TEXT"),
        ("other_irrig_timing", "TEXT"),
        ("other_irrig_rainfall_dep", "TEXT")
    ]
    
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE farmer_data ADD COLUMN {col_name} {col_type}")
            print(f"Added column: {col_name}")
        except sqlite3.OperationalError:
            print(f"Column already exists: {col_name}")
            
    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == '__main__':
    migrate()
