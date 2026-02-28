1) ETL vs ELT (and why ELT usually wins in cloud)
ETL (Extract → Transform → Load)
Transform happens before the warehouse/lakehouse.
You pull data out of source
Transform in Spark/ETL tool
Load final shaped tables into DW
When it still makes sense
PII masking/tokenization must happen before landing (policy/regulatory)
Source systems are fragile and can’t handle repeated reads; you want one pull + transform
You’re loading into a DW that’s expensive for transforms (less common now)
ELT (Extract → Load → Transform)
Load raw/bronze first, transform inside the platform (Snowflake/BigQuery/Databricks/Synapse).
Extract from source → land raw
Transform via SQL models in the DW/lakehouse
Build marts for analytics
Why ELT usually wins in cloud
Scale on demand: warehouses/lakehouses are built for big SQL transforms
Faster iteration: change logic in SQL and re-run without re-extracting everything
Lineage & governance: raw is preserved; you can audit, debug, and backfill easily
Cost control: compute is separated; run transforms only when needed (and turn off)

Senior interview one-liner
“I prefer ELT in cloud because raw is immutable and reprocessing becomes a compute problem, not a data-availability problem.”

2) Staging → ODS → DW → Data Marts (the “why” and how it looks in real life)
Think in contracts and audiences:
A) Staging / Raw (Bronze)
Purpose: land data exactly as received (plus metadata).
Audience: data engineers, audits, backfills.
Example: raw.orders (JSON/CSV/Avro/Parquet)
payload (original fields) _ingested_at, _source_file, _batch_id, _checksum
minimal parsing, no business logic
Techniques
Partition by ingestion date (or event date if reliable)
Keep schema evolution tolerant (semi-structured ok)

B) ODS (Operational Data Store) / Clean (Silver)
Purpose: cleaned, typed, deduped, standardized entities close to source truth.
Audience: downstream transformations, operational reporting.
Example: ods.orders
Correct types, standardized timezones/currencies
Removed duplicates by business keys
Late-arriving updates handled
Techniques
Standardize nulls, enums, timestamps
De-duplicate using event-time + versioning (more below)

C) DW (Gold / Core Warehouse)
Purpose: integrated, conformed model for analytics (facts/dims).
Audience: BI, analytics, ML features.
Example:
dw.fact_orders (grain: one row per order)
dw.dim_customer, dw.dim_product
conformed dimensions shared across domains
Techniques
Surrogate keys, SCD where needed
Strong grain definition + constraints

D) Data Marts (Semantic layer / Curated outputs)
Purpose: optimized for a specific team/use case.
Audience: business users.
Example: mart.finance_revenue_daily, mart.marketing_cohorts
pre-aggregations, business-ready metrics
metric definitions consistent + documented
Techniques
Precompute expensive metrics (P95/P99, cohorts)
“Thin marts”: mostly views if performance allows, tables if not
Senior signal
“ODS is for clean source-aligned truth; DW is for integrated conformed truth; marts are for business consumption.”

3) Idempotency (non-negotiable for seniors)
Idempotent pipeline = you can run the same job multiple times and get the same result.
Patterns to implement idempotency
Pattern 1: “Overwrite by partition” (best for batch on date-based data)
Target tables partitioned by dt (event_date)
Each run recomputes affected partitions and overwrites them
Example: recompute last 7 days daily aggregates
determine affected_dates

INSERT OVERWRITE / MERGE to those partitions only
Simple, reliable
Requires stable partition key and bounded backfill

Pattern 2: MERGE/UPSERT by natural key (best for CDC-like tables)
Use a unique key (order_id, customer_id)
MERGE INTO with deterministic rules
Handles updates
Must define “latest record wins” correctly (timestamp/version)

Pattern 3: Immutable + “latest view”
Append-only table of changes (events or snapshots)
Consumers read a view that picks latest per key
Great auditability
Needs optimization for query performance
Senior interview line
“I assume reruns will happen, so every layer is either partition-overwrite or merge-idempotent, and every job has a deterministic watermark strategy.”

4) Reprocessing & Backfills (how seniors do it without chaos)
Common reasons
Late arriving data
Bug in transformation logic
Upstream schema change
Historical correction from source
The senior approach: Backfill is a product feature
You build:
Backfill modes
--mode=incremental
--mode=backfill --start=2026-01-01 --end=2026-01-31
Audit table
run_id, start/end, status, row_counts, checks
Deterministic inputs
raw is immutable + versioned
Recompute only affected partitions
never “truncate everything” unless truly required
Practical technique: “Lookback window”
Even incremental jobs reprocess a small window to catch late events.
Example: orders can arrive up to 3 days late
Always reprocess last N=3 days

5) Hands-on architecture: Raw → Clean → Curated layers
Real-time example scenario: E-commerce Orders + Payments
Sources
orders_service (orders created/updated)
payments_gateway (payment status)
shipment_service (shipment milestones)
Goal
Daily revenue dashboard
Order fulfillment SLA metrics
Finance reconciliation
Flow
Raw
raw.orders_events, raw.payments_events, raw.shipments_events (append-only)
Clean/ODS
ods.orders_current (latest state per order_id)
ods.payments_current
DW
dw.fact_orders (conformed metrics: net_amount, discount, tax)
dw.fact_shipments
dw.dim_customer, dw.dim_date
Marts
mart.revenue_daily
mart.sla_breaches_daily

6) SQL transformations inside DW (what interviewers want to hear)
What you should push into SQL (ELT)
Standard joins between clean tables
Business rules that change often (e.g., “revenue = …”)
Dim/fact building
Aggregations that fit warehouse strengths
Best practices
Use incremental models (process only changed keys/partitions)
Prefer MERGE for SCD and upserts
Maintain data quality checks (row count deltas, null checks, uniqueness)
Example: build a current-state ODS table (pseudo SQL)
Deduplicate raw events → pick latest per order_id using row_number() ordered by event_time and ingested_at
Merge into ods.orders_current

7) PySpark for heavy joins, large aggregations, dedup (how to decide)
Use PySpark when
Join sizes are massive and you need:
broadcast strategy control
skew handling
repartitioning and bucketing tactics
Aggregations are huge (billions of rows) and SQL engine struggles/cost spikes
Dedup logic needs complex parsing, UDF-free but multi-step workflows
Techniques seniors mention (and interviewers love)
Heavy joins
Broadcast small dimension tables
Repartition by join keys before join (avoid shuffle storms)
Handle data skew:
salting keys
AQE (if Spark 3+)
Use join hints carefully (if supported)
Large aggregations
Pre-aggregate early (map-side combine effect)
Use correct partitioning for groupBy keys
Watch shuffle partitions + file sizes
Deduplication
Define deterministic ordering:
row_number() over (business_key) order by (event_time desc, ingested_at desc)
Keep a rejects table for bad records (schema errors, missing keys)

8) The senior signal: “I design pipelines assuming re-runs will happen.”
My pipeline design principles
Raw is immutable, always recoverable
Every job is idempotent
Incremental logic uses watermarks + lookback
Backfills are supported by design (date range + affected partitions)
Each run writes to an audit/run table
I implement data quality gates before publishing curated/marts
A strong 30-second answer
“I build ELT-first pipelines: land immutable raw with metadata, produce clean ODS with dedup and typing, then conformed DW facts/dims and business marts. Every step is idempotent via partition overwrite or merge, and I always support reruns and backfills using date-range reprocessing and a lookback window for late-arriving data.”

Interview-ready checklist (memorize this)
✅ Define grain at each layer
✅ Explain idempotency pattern you use (overwrite partitions / merge)
✅ Explain incremental strategy (watermark + lookback)
✅ Explain backfill strategy (range-based, audit, recompute affected partitions)
✅ Explain when SQL vs Spark (cost, scale, skew, complexity)
✅ Mention data quality + observability (counts, freshness, uniqueness, nulls)