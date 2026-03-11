import sqlite3
import os

def migrate():
    possible_paths = [
        os.path.join(os.getcwd(), 'farmer_app.db'),
        os.path.join(os.getcwd(), 'backend', 'farmer_app.db')
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
            
    if not db_path:
        print(f"Database not found in possible locations: {possible_paths}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    new_columns = [
        ('loan_source', 'TEXT'),
        ('repay_on_time', 'INTEGER'),
        ('crop_loss_earlier', 'INTEGER'),
        ('farming_only_income', 'INTEGER'),
        ('other_income_sources', 'INTEGER'),
        ('save_after_harvest', 'INTEGER'),
        ('saving_location', 'TEXT'),
        ('invested_equipment', 'INTEGER'),
        ('digital_payment_usage', 'INTEGER'),
        ('check_market_price', 'INTEGER'),
        ('risk_try_new_methods', 'INTEGER'),
        ('risk_afraid_loss', 'INTEGER'),
        ('risk_follow_neighbors', 'INTEGER')
    ]

    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE farmer_data ADD COLUMN {col_name} {col_type}")
            print(f"Added column: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists.")
            else:
                print(f"Error adding column {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Migration completed!")

if __name__ == '__main__':
    migrate()
