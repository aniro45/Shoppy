import os
import sqlite3

def check_sqlite_db(db_path='shopEase.db'):
    """Simple script to directly check SQLite database"""
    abs_path = os.path.abspath(db_path)
    
    print(f"Checking SQLite database at: {abs_path}")
    
    if not os.path.exists(abs_path):
        print(f"Database file not found at {abs_path}")
        
        # Check if it exists in any of the parent directories
        current = os.getcwd()
        parent_dirs = []
        for _ in range(3):  # Check up to 3 parent directories
            parent = os.path.dirname(current)
            if parent == current:  # Root directory reached
                break
            current = parent
            parent_dirs.append(current)
        
        for parent in parent_dirs:
            potential_path = os.path.join(parent, db_path)
            if os.path.exists(potential_path):
                print(f"Database found at: {potential_path}")
                abs_path = potential_path
                break
        else:
            # Check for any .db files in the current directory
            db_files = [f for f in os.listdir('.') if f.endswith('.db')]
            if db_files:
                print(f"Found other database files: {db_files}")
                # Use the first one found
                abs_path = os.path.abspath(db_files[0])
                print(f"Will use: {abs_path}")
            else:
                print("No .db files found in the current directory.")
                return
    
    try:
        conn = sqlite3.connect(abs_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("Database exists but contains no tables.")
            return
            
        print(f"Found {len(tables)} tables:")
        
        # Check each table
        for table_name in [t[0] for t in tables]:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"  - Table '{table_name}': {count} rows")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                print(f"    Sample data: {rows}")
        
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

if __name__ == "__main__":
    check_sqlite_db()
    
    # Also try with absolute path from config
    try:
        from config import Config
        if 'sqlite:///' in Config.SQLALCHEMY_DATABASE_URI:
            db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
            if db_path.startswith('/'):
                # It's an absolute path
                print("\nAlso checking database path from config:")
                check_sqlite_db(db_path)
    except ImportError:
        print("Could not import Config to check database path")
