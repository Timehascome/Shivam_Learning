# Spark File Formats (Quick Revision)

## CSV (Comma Separated Values)

- **Data Structure:** CSV is a plain text, **row-based** format where values are separated by commas and each row represents a record. It's human-readable.
- **Read:** Generally slower for large datasets due to row-based nature and lack of indexing. All rows and columns need to be read even if only a subset is required.
- **Write:** Simple to write.
- **Compute:** Requires parsing of strings, which can be computationally intensive.
- **Storage:** Can be inefficient for large datasets as it stores all data as text, leading to larger file sizes. Does not support **complex data structures or schema enforcement**.
- **Advantages:** Widely supported and human-readable, making it easy for data sharing.
- **Disadvantages:** Lacks schema enforcement, poor compression, and inefficient for analytical queries on large datasets.

---

## JSON (JavaScript Object Notation)

- **Data Structure:** JSON is a human-readable, text-based format that supports nested structures like arrays and objects. It's semi-structured.
- **Read:** Can be slow for large datasets, especially if not partitioned or compressed, as it's typically read line by line.
- **Write:** Flexible and easy to write.
- **Compute:** Requires parsing for each record, which can be computationally heavy.
- **Storage:** More compact than CSV for complex data but still stores data as text, which is less efficient than binary formats.
- **Advantages:** Flexible schema, widely used for web APIs and real-time data exchange, and human-readable.
- **Disadvantages:** No **schema enforcement** by default (though inferable), less efficient for analytical querying compared to columnar formats, and can have larger file sizes.

---

## Avro (Apache Avro)

- **Data Structure:** Avro is a **row-based, binary** format that uses JSON for defining data types and serializes data in a compact binary format.  
  Each Avro file starts with a schema that describes the data structure.
- **Read:** Efficient for read-heavy operations where entire rows are needed. Supports schema evolution, allowing for additions or removals of fields without breaking existing pipelines.
- **Write:** Optimized for write-heavy operations and streaming data due to its row-based nature and **efficient serialization/deserialization**.
- **Compute:** Efficient serialization and deserialization, making it good for data transfer between systems.
- **Storage:** Compact binary format, leading to smaller file sizes than text-based formats.
- **Advantages:** **Schema evolution (backward and forward compatibility)**, language-neutral, and good for Kafka-based streaming and cross-platform data interchange.
- **Disadvantages:** Not ideal for analytical queries that only require a subset of columns due to its row-based nature.

+------------------------------------------------------+
|                  AVRO DATA FILE                      |
+---------------------+--------------------------------+
| Header              | Data Blocks                    |
| - Magic: "Obj"      | +----------------------------+ |
| - Metadata (JSON)   | | Block #1                   | |
|   • schema          | |  - record1 record2      | |
|   • codec           | |  - compressed as a block   | |
| - Sync marker (16B) | +----------------------------+ |
+---------------------+ +----------------------------+ |
                        | Block #2                   | |
                        |  - record               | |
                        +----------------------------+ |
                        |                          |
                        +----------------------------+ |
                        | Block #N                    |
                        +----------------------------+ |
How data is stored?
Row 1: [id=1, name="A", salary=1000]
Row 2: [id=2, name="B", salary=1500]
Row 3: [id=3, name="C", salary=2000]

When AVRO shines (mental picture)
Streaming / write-heavy pipelines (Kafka → storage)
Schema evolution (add/remove fields safely)
Reads often scan whole rows (not column pruning friendly)

---

## Parquet (Apache Parquet)

- **Data Structure:** Parquet is a **columnar** storage format, meaning data for each column is stored separately. It's a self-describing format that contains both data and metadata.  
  Parquet files are divided into **row groups**, and within each row group, data for each column is stored separately in **column chunks**, which are further divided into **pages**.
- **Read:** Highly efficient for analytical queries as it only reads the necessary columns, significantly reducing I/O. Supports **predicate pushdown**.
- **Write:** Good for batch processing and analytics.
- **Compute:** Optimized for data processing frameworks like Spark, leading to faster query execution.
- **Storage:** Achieves high compression ratios due to similar data types being stored together in columns, leading to significant storage savings (**2–5× reduction** compared to row-based formats).
- **Advantages:** Columnar storage (efficient I/O, better compression), supports schema evolution, efficient compression, and good for OLAP workloads.
- **Disadvantages:** Less optimal for frequent small updates or real-time writes. Not suitable for **transactional workloads**.

+------------------------------------------------------+
|                   PARQUET FILE                       |
+--------------------+---------------------------------+
| Header "PAR1"      | Row Group #1                   |
|                    |  +---------------------------+  |
|                    |  | Column Chunk: id          |  |
|                    |  |  - Page 1                 |  |
|                    |  |  - Page 2                 |  |
|                    |  +---------------------------+  |
|                    |  | Column Chunk: name        |  |
|                    |  |  - Page 1                 |  |
|                    |  +---------------------------+  |
|                    |  | Column Chunk: salary      |  |
|                    |  |  - Page 1                 |  |
|                    |  +---------------------------+  |
|                    +---------------------------------+
|                    | Row Group #2                 |
+--------------------+---------------------------------+
| Footer (metadata)  |  - schema, row group stats      |
| + Footer length    |  - min/max per column (stats)   |
+------------------------------------------------------+

Column id:     [1, 2, 3, ]
Column name:   ["A","B","C",]
Column salary: [1000,1500,2000,]

Query: SELECT AVG(salary) WHERE id BETWEEN 10 AND 100
Parquet can:
✅ Read only "salary" + "id" column chunks (column pruning)
✅ Skip pages/row-groups using min/max stats (predicate pushdown)
❌ Avoid reading "name" entirely

------

## ORC (Optimized Row Columnar)

- **Data Structure:** ORC is also a **columnar** storage format. It organizes data into **stripes**, and each stripe contains column data. Each column within a stripe has an index.
- **Read:** Optimized for read performance, especially in Hadoop and Hive ecosystems. Supports predicate pushdown and lightweight indexing, allowing for faster data retrieval.
- **Write:** Good for batch processing, especially in data warehousing environments.
- **Compute:** Designed for high performance and efficient storage.
- **Storage:** Offers high compression ratios and various compression algorithms (Snappy, Zlib, Gzip) which can be specified at the column level.
- **Advantages:** Columnar storage, high compression, **predicate pushdown**, advanced indexing (e.g., Bloom Filters), ACID transaction support. *(End of screenshot content.)*
- **Disadvantages:** Optimized for hadoop and hive ecosystem though spark has native support.

+------------------------------------------------------+
|                     ORC FILE                         |
+----------------------+-------------------------------+
| Header "ORC"         | Stripe #1                     |
|                      |  +--------------------------+ |
|                      |  | Index (per column)       | |
|                      |  +--------------------------+ |
|                      |  | Column data streams      | |
|                      |  |  - stream for id         | |
|                      |  |  - stream for name       | |
|                      |  |  - stream for salary     | |
|                      |  +--------------------------+ |
|                      |  | Stripe Footer (stats)    | |
|                      |  +--------------------------+ |
+----------------------+-------------------------------+
| Stripe #2                                          |
+------------------------------------------------------+
| File Footer (overall stats + schema + stripe map)     |
| Postscript (compression info, footer length, etc.)    |
+------------------------------------------------------+

ORC File
  ├─ Stripe 1  (like a big chunk)
  │    ├─ column indexes  (helps skipping)
  │    ├─ column streams  (actual compressed column data)
  │    └─ stripe stats
  ├─ Stripe 2
  └─ Stripe N

Why ORC can be very efficient?
Strong built-in indexing + stats
Very efficient for Hive-like ecosystems
Great compression + skipping capability on scans

**Spark chooses Parquet by default because Parquet is Spark-native, engine-agnostic, and optimized for Spark’s execution model, whereas ORC is Hive-centric and tightly coupled to Hive’s reader, indexing, and ACID design.**

------

 ##Sub Topics in deep for ORC vs Parquet:
 1) Predicate Pushdown
 >Parquet supports multi level pruning:
 File
 ├─ Row Group
 │    ├─ Column Chunk
 │    │    ├─ Pages
 │    │    │    ├─ Page-level stats (min/max)

Spark uses:
Row Group stats (min/max)
Page-level stats
Column pruning

>ORC has:
Stripe-level stats
Column indexes
Bloom filters (optional)
BUT:
Spark does not fully utilize ORC indexes
Bloom filters often ignored
ACID visibility complicates filtering
So Spark does:
Stripe-level pruning only
Less granular skipping
Less effective in Spark
Excellent in Hive (LLAP + Hive optimizer)

 2) Schema evolution vs enforcement
Parquet — Schema evolution (flexible)
Parquet stores schema in footer metadata.
Supports:
Add column ✅
Drop column ✅
Rename column ⚠️ (logical mapping)
Reorder columns ✅
Spark behavior:
spark.read.schema(new_schema).parquet(path)
Spark:
Matches columns by name
Missing columns → NULL
Extra columns → ignored
👉 Ideal for data lakes

🔹 ORC — Schema enforcement (Hive-style)
ORC assumes:
Schema defined in Hive Metastore
Reader must follow table schema
ACID tables enforce strict column behavior
Problems in Spark:
Spark ignores some Hive schema evolution rules
Column changes may cause read failures
Renames are painful
👉 Best when Hive controls schema lifecycle
Summary
Aspect         	   Parquet	             ORC
Schema flexibility	High	           Medium
Engine independence	Yes	             Hive-centric
Spark friendliness	High	             Low

 3) Complex data structures support and example
Complex Data Structures (Array, Map, Struct)
Both formats support:
array
map
struct
nested types
Example schema
user STRUCT<
  id INT,
  name STRING,
  addresses ARRAY<STRUCT<city STRING,zip INT>>

>Parquet — Columnar flattening
Internally:
Each nested field stored as a column Uses definition & repetition levels
Spark:
Efficient nested column pruning
Reads only required nested fields
Example:
SELECT  ser.addresses.city FROM users;
Spark reads:
Only addresses.city column
✅ Very efficient in Spark

>ORC — Stream-based nesting
Each field stored as a separate stream
More metadata streams
Hive understands this deeply
Spark:
Can read complex types
But nested pruning less efficient than Parquet
Summary
Aspect	                 Parquet        	ORC
Nested pruning in Spark	Excellent	       Good
Hive support	         Good	         Excellent


4️⃣ Transactional Workloads  (CRITICAL difference)
>ORC — Built for transactions (Hive ACID)
ORC supports:
INSERT
UPDATE
DELETE
MERGE
How?
Base files
Delta files
Delete delta files
Snapshot isolation
Base ORC
+ Delta Insert
+ Delta Delete
Used by:
Hive ACID tables
LLAP
❌ Spark cannot fully write ORC ACID
❌ Spark ignores transaction metadata


>Parquet — NOT transactional
Parquet:
Immutable
Append-only
No row-level mutation
Transactions handled by:
Delta Lake
Iceberg
Hudi (all use Parquet)
👉 Spark prefers format + transaction layer separation
Summary
Aspect	             Parquet	       ORC
Native-transactions	     ❌	         ✅
Spark compatibility	  Via Delta	      ❌
Hive compatibility	  Limited	     Excellent

 5) ser vs deser in formats
>Parquet — Vectorized execution friendly
Parquet:
Columnar binary
Batch reads
JVM off-heap friendly
Works with Spark Tungsten
Spark:
Reads in batches (column vectors)
WholeStageCodegen applies
✅ Faster CPU usage
✅ Lower GC
✅ Better cache locality

>ORC — SerDe tied to Hive execution
ORC:
Optimized for Hive operators
Hive vectorization works great
Spark vectorization is less mature
Result:
Higher CPU overhead in Spark
Less predictable performance

6️) Why ORC is optimized for Hive but not Spark (CORE ANSWER)

ORC assumes	                  Spark reality
Hive Metastore is central	Spark can be metastore-less
ACID tables	                Spark prefers immutable files
Query engine = Hive	Spark   uses Catalyst
Index-heavy	                Spark prefers scan + prune
Stateful readers	        Spark prefers stateless readers

>Spark philosophy            
Simple files + smart engine

>Hive philosophy
Smart files + simpler engine


➡ ORC = Smart file
➡ Parquet = Smart engine

Final one-line takeaway :
Parquet aligns with Spark’s execution model (Catalyst + Tungsten + vectorized scans), while ORC aligns with Hive’s execution model (ACID + metastore + indexing). Spark prefers Parquet because Spark optimizes computation, not storage semantics.
-----------

 ##Partitioning Strategy in projects for files:
 =============================================
>Partitioning = directory-level data organization that allows Spark to skip files at read time.Spark does not read file content to filter partitions.
It prunes directories before scanning files.

s3://datalake/events/
  ├── country=IN/
  │    ├── year=2025/
  │    │    ├── month=01/
  │    │    │    ├── part-0001.parquet
  │    │    │    └── part-0002.parquet

| Concept            | Partitioning   | Bucketing    |
| ------------------ | -------------- | ------------ |
| Level              | File system    | Inside files |
| Implemented by     | Directories    | Hashing      |
| Used for           | Filter pruning | Joins        |
| Works without Hive | ✅            | ❌           |
| Spark usage        | **Very high**  | Low          |

Rule 1: Partition only on low cardinality columns
Rule 2: Partition on filter columns
Typical partitioning strategies (REAL PROJECTS)
1. Time-based partitioning (MOST COMMON) >> year=YYYY/month=MM/day=DD
2. Time + Dimension partitioning >> country + date
s3://sales/
  └── country=IN/year=2025/month=01/

>> How Spark uses partition pruning (internal flow)
Query:
SELECT * FROM sales
WHERE country='IN' AND year=2025

Spark Plan:
1. Read table metadata
2. Identify matching partition paths
3. Skip all other directories
4. Read only matching Parquet files

>>Streaming projects partitioning
df.writeStream \
  .partitionBy("date") \
  .format("parquet") \
  .option("path", path) \
  .start()

>>Partition evolution problem (real issue)
year=2020 → few partitions
year=2025 → huge partitions

**Summary** : 
Use time-based partitioning as the primary strategy.
Add one business dimension only if it significantly reduces scan size.
Maintain file sizes between 128–512 MB using controlled repartitioning.
Avoid high-cardinality columns as partition keys.
Partitioning reduces I/O by skipping directories before file scans, while Parquet reduces I/O inside files through column pruning and predicate pushdown. Both together give optimal Spark performance.


 ##Real time pyspark code snippets hands on git:
 ==================================================   
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import col
data =[(1,"Alice",30,"New York",100.50,"Electronics"),
    (2,"Bob",25,"Los angeles",200.75,"Books"),
    (3,"Charlie",35,"NEW York",150.00,"Electronics"),
    (4,"David",40,"Chicago",50.25,"Food"),
    (5,"Eve",28,"Los angeles",300.00,"Books"),
    (6,"Frank",32,"NEW York",120.00,"Electronics"),
    (7,"GRACE",22,"Houston",220.00,"Apparel"),
    (8,"Heidi",45,"Los angeles",250.00,"Books"),
    (9,"Heidi",45,"Los angeles",250.00,"Books"),
    (10,"Heidi",45,"Los angeles",250.00,"Books")]
schema =StructType([StructField("id", IntegerType(), True),StructField("name", StringType(), True),StructField("age", IntegerType(), True),StructField("city", StringType(), True),StructField("amount", DoubleType(), True),StructField("category", StringType(), True)])
df = spark.createDataFrame(data,schema)
df.show(5)
path_output = r"C:/Users/399sh/Downloads/Learning/Spark"
df.write.mode("overwrite").option("header", "true").csv(f"{path_output}/overwrite")
df.write.mode("overwrite").option("header", "true").option("compression","gzip").partitionBy("city").csv(f"{path_output}/overwrite")
>>> df.repartition(4).write.mode("overwrite").option("header", "true").csv(f"{path_output}/overwrite")
>>> df.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{path_output}/overwrite")

**read csv realworld**
df_csv = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", ",") \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("mode", "PERMISSIVE") \
    .csv("s3://raw-bucket/sales_csv/")
