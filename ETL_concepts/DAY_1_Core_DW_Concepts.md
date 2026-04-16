Concepts:
What is a Data Warehouse vs Data Lake vs Lakehouse
OLTP vs OLAP (write vs read optimization)
Fact tables vs Dimension tables
Grain (most misunderstood concept)
Star schema vs Snowflake schema
Additive, semi-additive, non-additive facts

Hands-on (SQL):
Design a Sales DW
fact_sales(order_id, date_id, product_id, customer_id, revenue, qty)
dim_date, dim_product, dim_customer

Write queries:
Daily revenue
Monthly revenue by product
Revenue by customer segment

***********************************************************************************
1) Data Warehouse vs Data Lake vs Lakehouse
Data Warehouse (DW):
Purpose: Fast, reliable analytics & BI on cleaned, modeled, structured data.
Data shape: “Schema-on-write” (you model it before loading).
Strengths: Consistency, governance, performance for SQL/reporting.
Typical workloads: KPIs, dashboards, finance reporting.
A data mart is a type of data warehouse that contains data specific to a particular business line or department rather than an entire enterprise.
self serviced analytics ; data driven decision making
Examples: Snowflake, Amazon Redshift, Google BigQuery.

2) Data Lake
Purpose: Store all data types (structured/semi-structured/unstructured) in raw/native form, cheaply at scale.
Data shape: “Schema-on-read” (apply structure when you query/process).
Strengths: Flexibility, ML/DS, long-term raw retention.
Tradeoff: Without strong governance, lakes can become “data swamps”.
Good vendor-neutral explainer : https://www.ibm.com/think/topics/data-warehouse-vs-data-lake-vs-data-lakehouse?utm_source=chatgpt.com
Examples: AWS S3, Azure Data Lake, Hadoop HDFS.

3) Lakehouse
Purpose: Combine lake’s cheap open storage + warehouse-like reliability/performance.
Key idea: Data on lake storage but with ACID tables, governance, and SQL performance (often via table formats like Delta/Iceberg/Hudi).
Databricks lakehouse definition: “combines benefits of lakes and warehouses.”
Interview one-liner:
Warehouse = trusted analytics store; Lake = raw flexible store; Lakehouse = lake + warehouse behaviors (ACID + governance + performance) on open storage.
Examples: Databricks Lakehouse (Delta Lake), Apache Iceberg, Snowflake Unistore.

Good learning links (high signal):
[Databricks: “Data lakes vs data warehouses”](https://www.databricks.com/blog/data-lakes-vs-data-warehouses-what-your-organization-needs-know?utm_source=chatgpt.com)
[AWS: “Difference between data warehouse and data lake”](https://aws.amazon.com/compare/the-difference-between-a-data-warehouse-data-lake-and-data-mart/?utm_source=chatgpt.com)
[Databricks docs: “What is a lakehouse?”](https://docs.databricks.com/aws/en/lakehouse/?utm_source=chatgpt.com)
****************************************************************************************************************************************
4) OLTP vs OLAP (write vs read optimization)
OLTP (Online Transaction Processing)
Goal: Correctness + fast small writes/reads (INSERT/UPDATE per transaction).
Modeling: **Normalized** (3NF), avoids redundancy.
Patterns: Many concurrent users, point lookups, row-level updates.
Indexes: Optimize for selective lookups; heavy constraints.

OLAP (Online Analytical Processing)
Goal: Fast reads over large scans/aggregations.
Modeling: Dimensional (star/snowflake), denormalized dimensions.
Patterns: Fewer users but big queries: GROUP BY, joins to dims, windowing.
Optimization: Partitioning (by date), columnar storage (in modern systems), pre-aggregations.

Interview punchline: OLTP optimizes “many tiny transactions”; OLAP optimizes “fewer heavy aggregations”.

**************************************************************************************************************
5) Fact tables vs Dimension tables:

Fact table:
Central table of a business process measurement/events.
Contains:
Foreign keys to dimensions (date_id, product_id, customer_id…)
Measures (revenue, qty, discount…)
Kimball definition style: fact table = keys + measurements.

Dimension table
Descriptive context for slicing/dicing facts.
Examples: product category/brand, customer segment, date attributes.

Common interview trap: Putting “attributes” (like customer segment) inside the fact table → kills reusability and SCD handling.
https://www.kimballgroup.com/2003/01/fact-tables-and-dimension-tables/?utm_source=chatgpt.com

******************************************************************************************************************************
6) Grain (most misunderstood) ✅
Grain = what ONE ROW of the fact table represents.
Example grains:
“One row per order line” (order_id + product_id)
“One row per order”
“One row per customer per day snapshot”

Why it matters:
Determines what’s legal to sum/average.
Prevents double-counting.
Drives keys and dimensional joins.
Rule: Declare grain before choosing facts/measures. (Kimball techniques emphasize grain declaration early.)
***********************************************************************************************************************************

5) Star schema vs Snowflake schema
Star schema
Dimensions are denormalized (wider dim tables).
Fewer joins, simpler, often faster for BI.
Preferred default for most DW reporting.

Snowflake schema
Dimensions normalized into sub-dimensions (e.g., dim_product → dim_category).
Pros: reduces redundancy, can improve dim maintenance.
Cons: more joins, more complex queries.

Interview answer: Start with star unless you have strong reasons (very large shared hierarchies, governance needs, extreme redundancy).

********************************************************************************************************************************************
6) Additive vs Semi-additive vs Non-additive facts *
Kimball’s canonical categories:
Additive
Can sum across all dimensions (including time)
Example: revenue, qty
Semi-additive
Can sum across many dims but not time
Example: account balance, inventory on-hand (you don’t sum balances across days; you take last/avg/min/max)
Non-additive
Cannot be summed meaningfully
Example: ratios (conversion_rate), percentages, averages (need numerator/denominator strategy)

Interview tip: For non-additive facts, store components (e.g., clicks, impressions) then compute rate.

*********************************************************************************************************************************************

7) CREATE DATABASE IF NOT EXISTS sales_dw;
USE sales_dw;

-- Dimensions
CREATE TABLE dim_date (
  date_id      INT PRIMARY KEY,           -- e.g., 20260209
  full_date    DATE NOT NULL,
  day          TINYINT NOT NULL,
  month        TINYINT NOT NULL,
  month_name   VARCHAR(10) NOT NULL,
  year         SMALLINT NOT NULL
);

CREATE TABLE dim_product (
  product_id   INT PRIMARY KEY,
  product_name VARCHAR(100) NOT NULL,
  category     VARCHAR(50) NOT NULL,
  brand        VARCHAR(50) NOT NULL
);

CREATE TABLE dim_customer (
  customer_id  INT PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  segment      VARCHAR(30) NOT NULL,       -- e.g., Retail/SMB/Enterprise
  city         VARCHAR(50) NOT NULL
);

-- Fact (grain: one row per order_id per product_id per day)
CREATE TABLE fact_sales (
  order_id     BIGINT NOT NULL,
  date_id      INT NOT NULL,
  product_id   INT NOT NULL,
  customer_id  INT NOT NULL,
  revenue      DECIMAL(12,2) NOT NULL,
  qty          INT NOT NULL,
  PRIMARY KEY (order_id, product_id),      -- assumes 1 line per product per order
  KEY idx_fs_date (date_id),
  KEY idx_fs_prod (product_id),
  KEY idx_fs_cust (customer_id),
  CONSTRAINT fk_fs_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
  CONSTRAINT fk_fs_prod FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  CONSTRAINT fk_fs_cust FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);
*********DATA************
INSERT INTO dim_date VALUES
(20260201,'2026-02-01',1,2,'Feb',2026),
(20260202,'2026-02-02',2,2,'Feb',2026),
(20260215,'2026-02-15',15,2,'Feb',2026),
(20260301,'2026-03-01',1,3,'Mar',2026);

INSERT INTO dim_product VALUES
(101,'Running Shoes','Footwear','Nike'),
(102,'Sports Watch','Wearables','Garmin'),
(103,'Yoga Mat','Fitness','Decathlon');

INSERT INTO dim_customer VALUES
(1,'Amit','Retail','Hyderabad'),
(2,'Meena','SMB','Bengaluru'),
(3,'Kiran','Enterprise','Mumbai');

INSERT INTO fact_sales VALUES
(9001,20260201,101,1,4999.00,1),
(9002,20260201,103,1, 899.00,1),
(9003,20260202,102,2,19999.00,1),
(9004,20260215,101,3,14997.00,3),
(9005,20260301,103,2, 1798.00,2);

****************queries***********
>>Daily revenue
SELECT
  d.full_date,+
  SUM(f.revenue) AS daily_revenue
FROM fact_sales f
JOIN dim_date d ON d.date_id = f.date_id
GROUP BY d.full_date
ORDER BY d.full_date;


>>Monthly revenue by product
SELECT
  d.year,
  d.month,
  p.product_name,
  SUM(f.revenue) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d    ON d.date_id = f.date_id
JOIN dim_product p ON p.product_id = f.product_id
GROUP BY d.year, d.month, p.product_name
ORDER BY d.year, d.month, monthly_revenue DESC;

>>Revenue by customer segment
SELECT
  c.segment,
  SUM(f.revenue) AS segment_revenue
FROM fact_sales f
JOIN dim_customer c ON c.customer_id = f.customer_id
GROUP BY c.segment
ORDER BY segment_revenue DESC;
