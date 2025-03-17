from app import create_app, db
from app.models import Product, Customer, Order
import random
import sys
import os
from sqlalchemy import inspect, text
import sqlite3

def check_db_file():
    """Check if the database file exists and print its path"""
    db_path = 'shopEase.db'  # Default relative path
    abs_path = os.path.abspath(db_path)
    
    print(f"Looking for database at: {abs_path}")
    if os.path.exists(abs_path):
        print(f"Database file exists (size: {os.path.getsize(abs_path)} bytes)")
        # Try to open it directly with sqlite3
        try:
            conn = sqlite3.connect(abs_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Direct SQLite check - Tables found: {tables}")
            conn.close()
        except Exception as e:
            print(f"Error connecting directly to SQLite: {str(e)}")
    else:
        print("Database file does not exist!")
        
        # Check the current working directory
        print(f"Current working directory: {os.getcwd()}")
        print("Files in current directory:")
        for file in os.listdir('.'):
            if file.endswith('.db'):
                print(f"  - {file} (size: {os.path.getsize(file)} bytes)")

def seed_database():
    try:
        print("Seeding database with dummy data...")
        
        # Create dummy products
        products = [
            Product(name="Smartphone", price=699.99, description="Latest model smartphone with high-end camera"),
            Product(name="Laptop", price=1299.99, description="Powerful laptop for work and gaming"),
            Product(name="Headphones", price=199.99, description="Noise cancelling wireless headphones"),
            Product(name="Smart Watch", price=349.99, description="Fitness and health tracking smartwatch"),
            Product(name="Tablet", price=499.99, description="10-inch tablet with retina display"),
            Product(name="Camera", price=899.99, description="DSLR camera with multiple lenses"),
            Product(name="Gaming Console", price=499.99, description="Next-gen gaming console"),
            Product(name="Bluetooth Speaker", price=129.99, description="Portable waterproof speaker"),
            Product(name="Wireless Mouse", price=49.99, description="Ergonomic wireless mouse"),
            Product(name="External Hard Drive", price=89.99, description="1TB portable storage solution")
        ]
        
        # Create dummy customers
        customers = [
            Customer(name="John Doe", email="john@example.com", password="password123"),
            Customer(name="Jane Smith", email="jane@example.com", password="password456"),
            Customer(name="Michael Johnson", email="michael@example.com", password="password789"),
            Customer(name="Emily Brown", email="emily@example.com", password="passwordabc"),
            Customer(name="David Wilson", email="david@example.com", password="passworddef")
        ]
        
        # Add products and customers to the session
        db.session.add_all(products)
        db.session.add_all(customers)
        
        # Commit to get IDs
        print("Committing products and customers to database...")
        db.session.commit()
        print("Commit successful!")
        
        # Create dummy orders
        order_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
        orders = []
        
        for _ in range(15):
            customer = random.choice(customers)
            status = random.choice(order_statuses)
            order = Order(customer_id=customer.id, status=status)
            orders.append(order)
        
        # Add orders to the session
        db.session.add_all(orders)
        print("Committing orders to database...")
        db.session.commit()
        print("Commit successful!")
        
        print("Database seeded successfully!")
        print(f"Added {len(products)} products, {len(customers)} customers, and {len(orders)} orders.")
        
        # Verify data was actually inserted
        product_count = Product.query.count()
        customer_count = Customer.query.count()
        order_count = Order.query.count()
        print(f"Verification - Products: {product_count}, Customers: {customer_count}, Orders: {order_count}")
        
    except Exception as e:
        print(f"Error during database seeding: {str(e)}")
        db.session.rollback()
        raise

def inspect_database():
    """Inspect the SQLite database tables and their contents"""
    try:
        print("Inspecting database tables...")
        
        # Get the database URI from the app config
        from flask import current_app
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        print(f"Database URI: {db_uri}")
        
        # Get the inspector
        inspector = inspect(db.engine)
        
        # Get all table names
        tables = inspector.get_table_names()
        if not tables:
            print("No tables found in the database!")
            check_db_file()
            return
            
        print(f"Found {len(tables)} tables: {', '.join(tables)}\n")
        
        # For each table, show row count and sample data
        for table in tables:
            # Get row count
            row_count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"Table '{table}': {row_count} rows")
            
            # Show sample data (first 5 rows)
            if row_count > 0:
                rows = db.session.execute(text(f"SELECT * FROM {table} LIMIT 5")).fetchall()
                print(f"Sample data from '{table}':")
                for row in rows:
                    print(f"  {row}")
            print()
    except Exception as e:
        print(f"Error during database inspection: {str(e)}")

if __name__ == "__main__":
    try:
        print(f"Starting with arguments: {sys.argv}")
        print(f"Current working directory: {os.getcwd()}")
        
        app = create_app()
        
        # Print app config
        print(f"App database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        with app.app_context():
            # Check if the database file exists before doing anything
            check_db_file()
            
            # Check command line arguments
            if len(sys.argv) > 1 and sys.argv[1] == "--inspect":
                inspect_database()
            else:
                # First clear existing data
                print("Clearing existing data...")
                try:
                    Order.query.delete()
                    Product.query.delete()
                    Customer.query.delete()
                    db.session.commit()
                    print("Data cleared successfully")
                except Exception as e:
                    print(f"Error clearing data: {str(e)}")
                    db.session.rollback()
                
                # Then seed with new data
                seed_database()
                
                print("\nUse 'python seed_data.py --inspect' to check database tables")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
