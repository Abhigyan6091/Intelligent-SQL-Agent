# create_sample_db.py
import sqlite3

def create_db(path="example.db"):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    # Drop tables if exist
    c.execute("DROP TABLE IF EXISTS users;")
    c.execute("DROP TABLE IF EXISTS orders;")
    # Create tables
    c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        signup_date TEXT
    );
    """)
    c.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        created_at TEXT,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    # Seed sample rows
    users = [
        ("Alice", "alice@example.com", "2024-08-01"),
        ("Bob", "bob@example.com", "2024-09-15"),
        ("Charlie", "charlie@example.com", "2024-12-02"),
    ]
    c.executemany("INSERT INTO users (name,email,signup_date) VALUES (?,?,?);", users)
    orders = [
        (1, 19.99, "2025-01-06", "completed"),
        (1, 5.0, "2025-02-01", "completed"),
        (2, 100.0, "2025-03-10", "pending"),
        (3, 42.5, "2025-03-11", "completed"),
    ]
    c.executemany("INSERT INTO orders (user_id,amount,created_at,status) VALUES (?,?,?,?);", orders)
    conn.commit()
    conn.close()
    print(f"Created sample DB at {path}")

if __name__ == "__main__":
    create_db()
