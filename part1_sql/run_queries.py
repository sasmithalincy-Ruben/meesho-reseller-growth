import sqlite3
import csv

conn = sqlite3.connect("data/meesho_reseller.db")

with open("part1_sql/queries.sql", "r") as file:
    query = file.read()

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()

with open("part1_sql/output/monthly_category_revenue.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["month", "category", "revenue", "n_orders"])

    writer.writerows(rows)

conn.close()

print("CSV file created successfully!")