# Task 1
 
import sqlite3

DB_PATH = "../db/lesson.db"

print("Task 1: ")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()

cur.execute("""
SELECT o.order_id,
       ROUND(SUM(p.price * li.quantity), 2) AS total_price
FROM orders AS o
JOIN line_items AS li ON li.order_id = o.order_id
JOIN products   AS p  ON p.product_id = li.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5;
""")
rows = cur.fetchall()
print(rows)
conn.close()



# Task 2

print("\nTask 2: ")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()

cur.execute("""
SELECT c.customer_name,
       ROUND(AVG(t.total_price), 2) AS avg_total_price
FROM customers AS c
LEFT JOIN (
    SELECT o.customer_id AS customer_id_b,
           o.order_id,
           SUM(p.price * li.quantity) AS total_price
    FROM orders AS o
    JOIN line_items AS li ON li.order_id = o.order_id
    JOIN products   AS p  ON p.product_id = li.product_id
    GROUP BY o.order_id
) AS t
ON c.customer_id = t.customer_id_b
GROUP BY c.customer_id
ORDER BY c.customer_name;
""")
rows = cur.fetchall()
print(rows)
conn.close()



# Task 3

print("\nTask 3: ")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()

try:
    conn.execute("BEGIN")

    cur.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons';")
    customer = cur.fetchone()
    cur.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris';")
    employee = cur.fetchone()
    cur.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5;")
    products = cur.fetchall()

    if customer and employee and len(products) == 5:
        cur.execute("INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, DATE('now'));",
                    (customer[0], employee[0]))
        order_id = cur.lastrowid
        for p in products:
            cur.execute("INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, 10);",
                        (order_id, p[0]))
        conn.commit()

        cur.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items AS li
        JOIN products AS p ON p.product_id = li.product_id
        WHERE li.order_id = ?
        ORDER BY li.line_item_id;
        """, (order_id,))
        rows = cur.fetchall()
        print("Created order_id:", order_id)
        print(rows)
    else:
        print("Something went wrong")
        conn.rollback()

except Exception as e:
    conn.rollback()
    print("Error:", e)

conn.close()



# Task 4

print("\nTask 4: ")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()

cur.execute("""
SELECT e.employee_id, e.first_name, e.last_name,
       COUNT(o.order_id) AS order_count
FROM employees AS e
JOIN orders AS o ON o.employee_id = e.employee_id
GROUP BY e.employee_id
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC, e.employee_id;
""")
rows = cur.fetchall()
print(rows)
conn.close()