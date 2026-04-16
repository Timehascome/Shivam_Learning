Concepts
Aggregate tables vs on-the-fly queries
Snapshot facts vs transaction facts
Late arriving facts
Slowly changing facts (yes, they exist)
Hands-on
Build:
Daily snapshot fact
Monthly aggregate fact
Compare:
Querying raw fact vs aggregate
*************************************************************************
>On-The-Fly Queries:
>You query raw transaction fact and compute aggregates at runtime.
>Aggregate Tables:
>You store aggregated results in a separate table.
>Transaction Fact Table: Each row = one event.
>fact_sales
------------------------------------
order_id | product_id | date_id | revenue

>Snapshot Fact Table:
Stores state at a point in time.
Example: Daily inventory
fact_inventory_snapshot
------------------------------------
date_id | product_id | stock_quantity

>Late Arriving Facts:
Fact arrives late compared to dimension.
Example:
Customer changed city yesterday
Sales data for last week arrives today
Problem:
Dimension version mismatch
Solution:
Surrogate keys
Effective_from / effective_to
Lookup by event timestamp

>Slowly changing facts:
Facts sometimes change.
Example:
Order initially $100
Later refunded to $80
If you overwrite:
You lose history.
order_id | revenue | adjustment_flag
1001     | -20     | 1
“Financial facts must preserve audit trail. I prefer adjustment rows over overwriting.”

>>CREATE TABLE fact_sales (
    order_id INT,
    product_id INT,
    date_id DATE,
    revenue DECIMAL(10,2)
);
INSERT INTO fact_sales VALUES
(1,101,'2026-02-01',100),
(2,101,'2026-02-01',200),
(3,102,'2026-02-02',150);
CREATE TABLE fact_sales_daily_snapshot AS
SELECT
    date_id,
    SUM(revenue) AS total_revenue,
    COUNT(order_id) AS total_orders
FROM fact_sales
GROUP BY date_id;
CREATE TABLE fact_sales_monthly_agg AS
SELECT
    DATE_FORMAT(date_id,'%Y-%m-01') AS month_start,
    SUM(revenue) AS monthly_revenue,
    COUNT(order_id) AS total_orders
FROM fact_sales
GROUP BY DATE_FORMAT(date_id,'%Y-%m-01');
SELECT DATE_FORMAT(date_id,'%Y-%m') AS month,
       SUM(revenue)
FROM fact_sales
GROUP BY month;
SELECT month_start, monthly_revenue
FROM fact_sales_monthly_agg;
“Aggregate tables reduce CPU and shuffle in distributed systems like Spark. In cloud warehouses, they reduce compute credits.”

Why are snapshot facts semi-additive?
How do you handle late arriving facts in SCD-2?
What happens if dimension version is missing?
How do you refresh aggregate tables?
What is fact grain?