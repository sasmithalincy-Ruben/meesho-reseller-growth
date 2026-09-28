import sqlite3
import csv

conn = sqlite3.connect("data/meesho_reseller.db")

query = """
SELECT
    r.region,
    SUM(o.quantity * o.unit_price) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
INNER JOIN resellers r
ON o.reseller_id = r.reseller_id
GROUP BY r.region;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()

with open("part1_sql/output/region_revenue.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["region", "revenue", "n_orders"])

    writer.writerows(rows)

conn.close()

print("Region CSV created successfully!")