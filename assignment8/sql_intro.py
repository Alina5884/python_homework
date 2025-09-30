import sqlite3
from pathlib import Path

db_dir = Path("../db")
db_dir.mkdir(parents=True, exist_ok=True)
db_path = db_dir / "magazines.db"

def add_publisher(cur, name):
    try:
        cur.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        pass

def get_publisher_id(cur, name):
    cur.execute("SELECT publisher_id FROM publishers WHERE name=?", (name,))
    row = cur.fetchone()
    return row[0] if row else None

def add_magazine(cur, name, publisher_name):
    pid = get_publisher_id(cur, publisher_name)
    if pid is None:
        add_publisher(cur, publisher_name)
        pid = get_publisher_id(cur, publisher_name)
    try:
        cur.execute("INSERT INTO magazines (name, publisher_id) VALUES (?,?)", (name, pid))
    except sqlite3.IntegrityError:
        pass

def add_subscriber(cur, name, address):
    cur.execute("SELECT 1 FROM subscribers WHERE name=? AND address=?", (name, address))
    if cur.fetchone():
        return
    try:
        cur.execute("INSERT INTO subscribers (name, address) VALUES (?,?)", (name, address))
    except sqlite3.Error:
        pass

def get_subscriber_id(cur, name, address):
    cur.execute("SELECT subscriber_id FROM subscribers WHERE name=? AND address=?", (name, address))
    row = cur.fetchone()
    return row[0] if row else None

def get_magazine_id(cur, name):
    cur.execute("SELECT magazine_id FROM magazines WHERE name=?", (name,))
    row = cur.fetchone()
    return row[0] if row else None

def add_subscription(cur, sub_name, sub_addr, mag_name, expiration_date):
    sid = get_subscriber_id(cur, sub_name, sub_addr)
    if sid is None:
        add_subscriber(cur, sub_name, sub_addr)
        sid = get_subscriber_id(cur, sub_name, sub_addr)
    mid = get_magazine_id(cur, mag_name)
    if mid is None:
        return
    cur.execute("SELECT 1 FROM subscriptions WHERE subscriber_id=? AND magazine_id=?", (sid, mid))
    if cur.fetchone():
        return
    try:
        cur.execute(
            "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?,?,?)",
            (sid, mid, expiration_date)
        )
    except sqlite3.IntegrityError:
        pass

try:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id),
            UNIQUE (subscriber_id, magazine_id)
        );
        """)

        add_publisher(cur, "Green Planet Media")
        add_publisher(cur, "Urban Life Press")
        add_publisher(cur, "Techie Times Co.")

        add_magazine(cur, "Eco Living", "Green Planet Media")
        add_magazine(cur, "Zero Waste Monthly", "Green Planet Media")
        add_magazine(cur, "City Vibes", "Urban Life Press")
        add_magazine(cur, "Gadgets Now", "Techie Times Co.")

        add_subscriber(cur, "Alice Johnson", "12 Ocean Ave, Brooklyn, NY")
        add_subscriber(cur, "Bob Smith", "44 Maple St, Queens, NY")
        add_subscriber(cur, "Charlie Kim", "9 Pine Rd, Manhattan, NY")

        add_subscription(cur, "Alice Johnson", "12 Ocean Ave, Brooklyn, NY", "Eco Living", "2026-03-01")
        add_subscription(cur, "Alice Johnson", "12 Ocean Ave, Brooklyn, NY", "Zero Waste Monthly", "2026-01-15")
        add_subscription(cur, "Bob Smith", "44 Maple St, Queens, NY", "City Vibes", "2025-12-31")
        add_subscription(cur, "Charlie Kim", "9 Pine Rd, Manhattan, NY", "Gadgets Now", "2026-06-30")

        print("Subscribers:")
        try:
            cur.execute("SELECT * FROM subscribers;")
            for r in cur.fetchall():
                print(r)
        except sqlite3.Error as e:
            print("Query error:", e)

        print("Magazines sorted by name:")
        try:
            cur.execute("SELECT * FROM magazines ORDER BY name;")
            for r in cur.fetchall():
                print(r)
        except sqlite3.Error as e:
            print("Query error:", e)

        print("Magazines for publisher 'Green Planet Media':")
        try:
            cur.execute("""
                SELECT m.magazine_id, m.name
                FROM magazines m
                JOIN publishers p ON m.publisher_id = p.publisher_id
                WHERE p.name = ?
            """, ("Green Planet Media",))
            for r in cur.fetchall():
                print(r)
        except sqlite3.Error as e:
            print("Query error:", e)

        conn.commit()
        print("Done")
    print("Connection closed")
except sqlite3.Error as e:
    print("Error:", e)