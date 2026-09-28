--Query 1: Revenue_by_month
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category;

--Query 2: Reseller Order Summary

SELECT
    r.region,
    SUM(o.quantity * o.unit_price) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
INNER JOIN resellers r
ON o.reseller_id = r.reseller_id
GROUP BY r.region;

--Query 3 :Top reseller by total spending

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

--Reseller who have never placed order
SELECT
    r.reseller_name,
    r.reseller_id
FROM resellers r
LEFT JOIN orders o
ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

----aov
SELECT
    month,
    ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';

