import sqlite3
import csv

conn = sqlite3.connect("data/meesho_reseller.db")

query = """
SELECT
    month,
    ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()

with open("part1_sql/output/aov_june_delivered.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["month", "aov"])

    writer.writerows(rows)

conn.close()

print("AOV CSV created successfully!")