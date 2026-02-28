Slowly Changing Dimensions
Concepts
SCD Type 0, 1, 2, 3, 4, 6
When NOT to use SCD 2
Storage explosion problem
Hands-on
SQL: Implement SCD-2 using effective_from, effective_to, is_current
PySpark: Merge incremental customer data using join + window + when

Expected Answer Level
“I use SCD-2 only for analytically relevant attributes. For noisy attributes, Type-1.”

==================================================================================================================================================
Attributes:
Analytically relevant (slow-changing): city, segment, marital_status
Noisy / not worth historizing (fast-changing): last_login_ts, mobile_app_version, marketing_opt_in (sometimes), support_ticket_count

Type 0 — “Fixed forever”
Use when: you truly need “as captured originally.”

Type 1 — “Overwrite”
Store only the latest value; no history.
Example: fixing spelling: cust_name from “Ramesh K” → “Ramesh Kumar”.
Use when: history is not analytically required or values are noisy.

Type 2 — “Full history (row versioning)”
New row per change with validity range and current flag.
Example: city: Pune → Hyderabad, you want revenue by customer city as-of purchase date.
Use when: point-in-time analysis is required.

Type 4 — “History table + current table”
One table has only current state (dim_customer_current)
Another table stores all changes (dim_customer_history)
Use when: you want current queries super fast + history retained separately.

Type 6 — “Hybrid (1+2+3 together)”
Often implemented as:
Type-2 row versioning AND
Type-3 columns like previous_city AND
Some Type-1 overwrite columns for noisy attributes
Example: Track full history of city (Type-2), keep previous_city (Type-3 convenience), overwrite email corrections (Type-1).

Lab: SQL and Pyspark;