import sqlite3
import csv

conn = sqlite3.connect("data/meesho_reseller.db")

query = """
SELECT
    r.reseller_name,
    r.reseller_id
FROM resellers r
LEFT JOIN orders o
ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()

with open("part1_sql/output/resellers_no_orders.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["reseller_name", "reseller_id"])

    writer.writerows(rows)

conn.close()

print("Resellers with no orders CSV created successfully!")