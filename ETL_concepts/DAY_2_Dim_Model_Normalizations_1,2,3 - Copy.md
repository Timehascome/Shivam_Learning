Concepts
Conformed dimensions
Degenerate dimensions
Role-playing dimensions (order date, ship date)
Junk dimensions
Factless fact tables
All normalization concepts.

Hands-on
Add:
order_status as degenerate dimension
promotion_flag + channel as junk dimension
Factless table: fact_student_attendance

Interview Angle
“What is the grain of your fact table and why?”

=======================================================================
1. Conformed Dimensions
Definition (Senior-Level)
A conformed dimension is a dimension shared across multiple fact tables with consistent structure and meaning, enabling cross-fact analysis.
It ensures:
Same surrogate keys
Same attributes
Same business definitions
Same hierarchy
This is the backbone of enterprise BI consistency.

fact_sales
fact_shipments
fact_returns
 If all the fact tables use dim_customer , then it is a conformed dimension
 
2. Degenerate Dimensions
Definition:
A degenerate dimension is a dimension attribute stored directly in the fact table without a separate dimension table.

Usually:
Transaction identifiers
Order numbers
Status codes
They have no additional descriptive attributes.

CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    date_id INT,
    quantity INT,
    revenue DECIMAL(10,2),
    order_status VARCHAR(20)  -- Degenerate dimension  (Completed ,Cancelled, Returned, Pending)
);
Note: Degenerate dimensions reduce schema complexity while preserving transaction identity.

3. Role-Playing Dimensions
Definition:
A role-playing dimension is when one dimension is reused multiple times in a fact table with different semantic meanings.
Eg: dim_date
→ order_date
→ ship_date
→ delivery_date
CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    order_date_id INT,
    ship_date_id INT,
    delivery_date_id INT,
    revenue DECIMAL(10,2),
    FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (ship_date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (delivery_date_id) REFERENCES dim_date(date_id)
);
Why  engineers use this
Because:
Date logic is centralized
Time intelligence is consistent
No duplicate dimension tables
BI tools treat them as separate roles.

4. Junk Dimensions
Definition:
A junk dimension combines low-cardinality flags and indicators into a single dimension.
Insted of :
dim_promotion_flag
dim_channel
dim_coupon_flag
dim_priority_flag

CREATE TABLE dim_order_context (
    context_id INT PRIMARY KEY,
    promotion_flag BOOLEAN,
    channel VARCHAR(20)
);
Why junk dimensions matter

They:
Reduce schema clutter
Improve query performance
Avoid many tiny dimension tables

5. Factless Fact Tables
Definition:
A factless fact table records events or relationships without numeric measures.
It answers:
Did something happen?
Not:
How much?
dim_student(student_id, name)
dim_class(class_id, subject)
dim_date(date_id, date)
CREATE TABLE fact_student_attendance (
    student_id INT,
    class_id INT,
    date_id INT,
    PRIMARY KEY (student_id, class_id, date_id),
    FOREIGN KEY (student_id) REFERENCES dim_student(student_id),
    FOREIGN KEY (class_id) REFERENCES dim_class(class_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

6. Normalization Concepts (Complete)
Normalization is a database design technique to:
Reduce redundancy
Prevent anomalies
Ensure data integrity
Improve maintainability
It mainly applies to OLTP systems, not warehouses.
Think of normalization as:
>>Breaking big messy tables into logically consistent smaller tables

1NF — First Normal Form
Rule
A table is in 1NF if:
Each column contains atomic values >> no more splittable
No repeating groups
Each row is unique

2NF — Second Normal Form
Rule
A table is in 2NF if:
It is in 1NF
**No partial dependency on composite keys**
OrderDetails
Bad Example: Primary key = (order_id, product_id) >> product_name → depends only on product_id >> This violates 2NF.
---------------------------------------
order_id | product_id | product_name
---------------------------------------
1        | 101        | Laptop

3NF — Third Normal Form
**Rule**
A table is in 3NF if:
It is in 2NF
**No transitive dependencies**>> What is transitive dependency?
A non-key column depends on another non-key column.
customer
--------------------------------
customer_id | city | country
--------------------------------
1           | NY   | USA
city → country

>Country depends on city, not customer.

BCNF — Boyce-Codd Normal Form
BCNF is a stronger version of 3NF.
Rule:
For every functional dependency:
A → B
A must be a candidate key.
>>BCNF fixes edge cases where 3NF still allows anomalies.

✅ 4NF — Fourth Normal Form
Rule
Remove multi-valued dependencies
student
------------------------
student | hobby | skill
If hobbies and skills are independent:
John → Guitar, Painting
John → Python, SQL
This creates unnecessary combinations.

student_hobby
student_skill

| Feature     | Normalization | Denormalization |
| ----------- | ------------- | --------------- |
| Redundancy  | Low           | High            |
| Write speed | Slower        | Faster          |
| Read speed  | Slower        | Faster          |
| Integrity   | Strong        | Weaker          |
| Use case    | OLTP          | OLAP            |

Here’s a polished senior answer:

In normalized schemas, writes are slower because inserting a single business event often requires multiple table writes, foreign key validation, index maintenance, and transactional coordination. Each of these operations adds I/O and locking overhead. While normalization improves data integrity and reduces redundancy, it introduces write amplification and concurrency bottlenecks. Denormalized systems trade some consistency for faster write throughput.