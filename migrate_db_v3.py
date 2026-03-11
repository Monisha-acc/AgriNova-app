import sqlite3
import os

def migrate():
    db_path = os.path.join(os.getcwd(), 'backend', 'farmer_app.db')
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE farmer_data ADD COLUMN enrolled_pmfby INTEGER")
        print("Added column: enrolled_pmfby")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column enrolled_pmfby already exists.")
        else:
            print(f"Error adding column enrolled_pmfby: {e}")

    conn.commit()
    conn.close()
    print("Migration completed!")

if __name__ == '__main__':
    migrate()
