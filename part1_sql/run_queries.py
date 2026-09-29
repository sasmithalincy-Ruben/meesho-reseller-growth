import sqlite3
import csv

conn = sqlite3.connect("data/meesho_reseller.db")

with open("part1_sql/queries.sql", "r") as file:
    query = file.read()

# queries.sql contains multiple SQL statements.
# The first statement is the monthly category revenue query.
statements = [statement.strip() for statement in query.split(";") if statement.strip()]
monthly_revenue_query = statements[0]

cursor = conn.cursor()
cursor.execute(monthly_revenue_query)

rows = cursor.fetchall()

with open(
    "part1_sql/output/monthly_category_revenue.csv",
    "w",
    newline=""
) as file:
    writer = csv.writer(file)
    writer.writerow(["month", "category", "revenue", "n_orders"])
    writer.writerows(rows)

conn.close()

print("Monthly category revenue CSV created successfully!")