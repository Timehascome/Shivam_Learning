# Apache Iceberg

## 1) What is Iceberg?
Apache Iceberg is an open table format for large analytic datasets stored in data lakes (for example, on Amazon S3).

It provides database-like table management on top of files such as Parquet/ORC/Avro, including:
- ACID transactions
- Schema evolution (add, rename, reorder columns safely)
- Partition evolution (change partition strategy without rewriting old data)
- Time travel (query older snapshots)
- Hidden partitioning (users query normal columns; engine handles partition details)

In short: Iceberg turns raw object storage into reliable, queryable, maintainable analytical tables.

## 2) Why Iceberg?
Without table formats, data lakes usually have problems:
- File listing is expensive and slow at scale
- No reliable concurrent writes
- Hard schema/partition changes
- No easy rollback/time-travel
- Data quality and governance are difficult

Why teams choose Iceberg:
- **Reliability**: atomic commits via metadata snapshots
- **Performance**: partition pruning and file-level statistics for skipping data
- **Engine interoperability**: works with Spark, Trino, Flink, Athena, etc.
- **Cost control**: compaction + metadata pruning reduce query and storage overhead
- **Governance**: easier auditing with snapshot history and reproducible reads

## 3) Real-world scenarios
1. **Event lakehouse for product analytics**
A company ingests clickstream events into S3 and uses Iceberg tables to support near-real-time dashboards and historical analysis with time travel.

2. **CDC from OLTP databases**
Debezium/Kafka captures updates from MySQL/PostgreSQL. Iceberg tables support upserts/merges and provide a clean analytics layer.

3. **Finance reconciliation and audit**
Daily P&L tables need exact reproducibility. Iceberg snapshot IDs allow re-running reports exactly as of a prior date.

4. **ML feature store backfill**
Data scientists need point-in-time correct training sets. Iceberg time travel helps create training data exactly as known at training time.

5. **Multi-engine analytics on one lake**
Data engineering writes with Spark, BI queries with Athena/Trino, and streaming jobs use Flink, all sharing the same Iceberg table format.

## 4) Internal working and interview questions

### Internal working (how Iceberg works)
- **Table metadata file**: root JSON that points to current snapshot, schema list, partition specs, sort orders, and properties.
- **Snapshot**: immutable version of table state. Each commit creates a new snapshot.
- **Manifest list**: file that points to one or more manifests used by a snapshot.
- **Manifest files**: contain data file entries and delete file entries with stats (min/max/null counts, partition values, record counts).
- **Data files**: actual Parquet/ORC/Avro files in object storage.
- **Delete files**:
  - Position deletes: delete specific row positions in data files.
  - Equality deletes: delete rows matching key columns.
- **Commit protocol**: optimistic concurrency. Writers create new metadata and atomically swap table pointer to new metadata if no conflict.
- **Query planning**:
  - Read current or chosen snapshot.
  - Use manifests and stats to prune irrelevant files.
  - Read only required data and apply deletes.

### Interview questions (with short answers)
1. **What problem does Iceberg solve in data lakes?**
It adds reliable table semantics (ACID, schema evolution, time travel, concurrent writes) on object storage.

2. **How is Iceberg different from plain Parquet on S3?**
Parquet is a file format; Iceberg is a table format that manages many Parquet files with metadata, snapshots, and transactions.

3. **What is a snapshot in Iceberg?**
An immutable table version created on each successful commit.

4. **Explain schema evolution in Iceberg.**
Columns are tracked with IDs, so rename/reorder operations are safe and do not break readers.

5. **What is partition evolution?**
You can change partition strategy over time without rewriting old partitions.

6. **How does Iceberg support time travel?**
By querying older snapshots using snapshot ID or timestamp.

7. **What are equality deletes vs position deletes?**
Equality deletes remove rows by key match; position deletes remove specific row positions in specific data files.

8. **How does concurrency control work?**
Optimistic concurrency with atomic metadata pointer swap; conflicting commits are retried/fail safely.

9. **How does Iceberg improve query performance?**
Manifest-level/file-level stats enable pruning; fewer files and row groups are scanned.

10. **Common operational maintenance tasks?**
Compaction, snapshot expiration, orphan file cleanup, metadata file pruning.

## 5) Demo project in AWS (hands-on)

### Project: Sales Lakehouse with Glue + S3 + Athena (Iceberg)
Goal: build an Iceberg table, perform inserts/updates/deletes, and run time-travel queries.

### Architecture
- **S3**: stores table data + Iceberg metadata
- **AWS Glue Data Catalog**: Iceberg catalog
- **AWS Glue ETL (Spark)**: create and mutate table
- **Amazon Athena**: query Iceberg table and snapshots

### Prerequisites
- AWS account
- S3 bucket (example: `s3://your-demo-bucket/iceberg-demo/`)
- IAM role for Glue with S3 + Glue + Athena permissions
- Athena workgroup configured

### Step-by-step
1. **Create database in Glue Catalog**
Use Athena or Glue console:
```sql
CREATE DATABASE IF NOT EXISTS demo_lakehouse;
```

2. **Create Iceberg table in Athena**
```sql
CREATE TABLE demo_lakehouse.sales_iceberg (
  order_id string,
  customer_id string,
  order_ts timestamp,
  amount double,
  region string
)
PARTITIONED BY (region)
LOCATION 's3://your-demo-bucket/iceberg-demo/sales_iceberg/'
TBLPROPERTIES ('table_type'='ICEBERG');
```

3. **Insert sample records**
```sql
INSERT INTO demo_lakehouse.sales_iceberg VALUES
('o1','c1',TIMESTAMP '2026-03-01 10:00:00',120.0,'IN'),
('o2','c2',TIMESTAMP '2026-03-01 11:00:00',450.0,'US'),
('o3','c3',TIMESTAMP '2026-03-02 09:30:00',300.0,'IN');
```

4. **Run update and delete**
```sql
UPDATE demo_lakehouse.sales_iceberg
SET amount = 500.0
WHERE order_id = 'o2';

DELETE FROM demo_lakehouse.sales_iceberg
WHERE order_id = 'o1';
```

5. **Query current state**
```sql
SELECT * FROM demo_lakehouse.sales_iceberg;
```

6. **Time travel query (before delete/update)**
In Athena Engine 3, use snapshot/time-travel syntax supported by your engine version. A common pattern is querying by snapshot ID after listing snapshots from Iceberg metadata tables.

7. **Inspect snapshots/metadata**
Use Iceberg metadata tables (for example `$snapshots`, `$history`, `$manifests`) to understand commits and file changes.

### What this demo teaches  
- Iceberg table creation and catalog registration
- DML operations (INSERT/UPDATE/DELETE) in a lake
- Snapshot-based time travel
- How metadata drives reliable and efficient queries

### Suggested extensions
- Add a Glue job for CDC upserts from a raw S3 landing zone
- Schedule compaction to reduce small files
- Add data quality checks before merge into Iceberg table
