import sqlite3
import datetime
import os

DB_NAME = "cafe.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    
    # 2. Menu Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL
        )
    ''')
    
    # 3. Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_amount REAL,
            date_time TEXT,
            staff_name TEXT
        )
    ''')
    
    # 4. Order Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            menu_item TEXT,
            quantity INTEGER,
            price_at_time REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    ''')
    
    # Seed a default admin user if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       ("admin", "admin123", "Admin"))
        
        # Seed some default menu items
        default_menu = [
            ("Espresso", "Coffee", 150.00),
            ("Latte", "Coffee", 200.00),
            ("Cappuccino", "Coffee", 180.00),
            ("Blueberry Muffin", "Snacks", 100.00),
            ("Chocolate Chip Cookie", "Snacks", 60.00),
            ("Cheesecake", "Desserts", 250.00)
        ]
        cursor.executemany("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)", default_menu)
        
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, password, role="Staff"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        return True, "Success"
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def get_menu_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM menu")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_menu_items(category=None):
    conn = get_connection()
    cursor = conn.cursor()
    if category and category != "All":
        cursor.execute("SELECT id, name, category, price FROM menu WHERE category=?", (category,))
    else:
        cursor.execute("SELECT id, name, category, price FROM menu")
    items = cursor.fetchall()
    conn.close()
    return items

def add_menu_item(name, category, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)", (name, category, price))
    conn.commit()
    conn.close()

def delete_menu_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

def create_order(staff_name, total_amount, items):
    """
    items should be a list of dicts: [{'name': 'Espresso', 'quantity': 2, 'price': 2.50}, ...]
    Returns the order ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("INSERT INTO orders (total_amount, date_time, staff_name) VALUES (?, ?, ?)",
                   (total_amount, timestamp, staff_name))
    order_id = cursor.lastrowid
    
    for item in items:
        cursor.execute("INSERT INTO order_items (order_id, menu_item, quantity, price_at_time) VALUES (?, ?, ?, ?)",
                       (order_id, item['name'], item['quantity'], item['price']))
        
    conn.commit()
    conn.close()
    return order_id, timestamp

def get_recent_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, total_amount, date_time, staff_name FROM orders ORDER BY date_time DESC LIMIT 50")
    orders = cursor.fetchall()
    conn.close()
    return orders

if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully.")
