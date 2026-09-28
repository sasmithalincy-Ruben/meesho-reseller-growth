import sqlite3
import csv

conn = sqlite3.connect("data/meesho_reseller.db")

query = """
SELECT
    r.reseller_name,
    r.reseller_id,
    r.region,
    SUM(o.quantity * o.unit_price) AS total_spend
FROM orders o
INNER JOIN resellers r
ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_name, r.reseller_id, r.region
ORDER BY total_spend DESC
LIMIT 5;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()

with open("part1_sql/output/top_reseller.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["reseller_name", "reseller_id", "region","total_spend"])

    writer.writerows(rows)

conn.close()

print("Top reseller CSV created successfully!")