1. MapReduce Fundamentals
What is MapReduce
Programming model for distributed batch processing
Designed for large-scale data on HDFS

Processes data using:
Map → transform
Shuffle & Sort → regroup
Reduce → aggregate

Why MapReduce Exists?
Handles data locality
Fault tolerant by design
Scales horizontally
Simplifies parallel programming

2. MapReduce Architecture
Core Components
Client
ResourceManager (YARN)
NodeManager
ApplicationMaster
Containers
HDFS (NameNode + DataNodes)

**Execution Flow**
Client
  ↓
YARN ResourceManager
  ↓
ApplicationMaster
  ↓
Map Tasks (on DataNodes)
  ↓
Shuffle & Sort
  ↓
Reduce Tasks
  ↓
HDFS Output

3. Map Phase (Deep Dive)

Input Format
Defines how input data is split
Examples:
TextInputFormat (default)
KeyValueTextInputFormat
SequenceFileInputFormat
CombineFileInputFormat (small files optimization)

Input Split vs HDFS Block
Block → physical storage (128MB)
Input Split → logical split
One Map Task per Input Split

RecordReader
Converts split → (key, value)
Key = offset (default)
Value = line content

Mapper
Stateless function
Emits intermediate key-value pairs
Should be lightweight
Avoid heavy joins

4. Combiner (Mini Reducer):
What is Combiner?
Runs after Map, before Shuffle
Reduces network I/O
Not guaranteed to run

Rules
Must be associative & commutative
Reducer logic reused safely

Example
Map output: (word, 1), (word, 1)
Combiner: (word, 2)

5. Shuffle & Sort (CRITICAL)
Shuffle
Transfers map output to reducers
Happens over network
Costliest phase
Sort
Map output sorted by key
Happens:
In-memory
On-disk spill
Merge phase
Partitioning
Determines which reducer gets which key
Default: hash(key) % numReducers
Custom partitioners improve data skew

6. Reduce Phase
Reducer Function

Input: (key, list(values))
Performs aggregation / business logic
Writes final output to HDFS
Reducer Output
One output file per reducer
Output is already sorted by key

7. MapReduce Job Lifecycle

Job submission

Input split generation

Map task execution

Spill to disk

Shuffle to reducers

Reduce execution

Output commit

Cleanup

8. Fault Tolerance

Map Task Failure

Retried on another node

Uses input split

Reduce Task Failure

Re-run entirely

Speculative Execution

Runs duplicate slow tasks

First successful one wins

9. Data Locality

Types

Node-local

Rack-local

Off-rack

Goal

Move compute to data

Reduce network traffic

🔟 Performance Tuning
Mapper Tuning
Increase mapreduce.map.memory.mb
Increase io.sort.mb
Use compression (Snappy)
Reducer Tuning
Right number of reducers
Avoid single reducer bottleneck
Shuffle Tuning
Compress map output
Use combiner
Increase parallel fetchers

11. Small Files Problem
Problem
Too many mappers
NameNode overload
Poor performance
Solutions
CombineFileInputFormat
HDFS HAR
Hive ORC/Parquet
HDFS distcp merge

12. Joins in MapReduce
Map-side Join
Requires sorted & partitioned data

Fastest join
Reduce-side Join

Default
Heavy shuffle

Broadcast Join
Small table distributed

13. Counters & Monitoring

Custom counters
Job history server
Task logs
Metrics via YARN

14. Limitations of MapReduce

High latency
Disk-heavy

Not suitable for:
Iterative algorithms
Streaming
Interactive queries

***🐝 HIVE — COMPLETE CONCEPTS**
1. Hive Basics
What is Hive

SQL layer on Hadoop
Translates SQL → MapReduce / Tez / Spark
Schema-on-read
Hive Use Cases
Batch analytics
ETL
Reporting
Data warehouse

2. Hive Architecture
Components

CLI / Beeline
Driver
Compiler
Optimizer
Execution Engine
Metastore

Execution Flow
SQL
 ↓
Parser
 ↓
Logical Plan
 ↓
Optimizer
 ↓
Physical Plan
 ↓
Execution (MR / Tez / Spark)

3. Hive Metastore
Stores

Table metadata
Column types
Partition info
SerDe info
Backed By

MySQL / Postgres / Derby

4. Managed vs External Tables
Feature       Managed	External
Data deletion	YES	      NO
Schema ownership	Hive	User
Use case	  Warehouse	 Shared data
Syntax
CREATE TABLE t1 (...);
CREATE EXTERNAL TABLE t2 (...) LOCATION 's3://...';

5. Partitioning

Why Partition
Reduce data scanned
Query pruning

Static Partition
INSERT INTO TABLE t PARTITION (dt='2026-01-01')

Dynamic Partition
SET hive.exec.dynamic.partition=true;

Best Practices

Low cardinality
Time-based

6. Bucketing
What is Bucketing

Hash-based split inside partitions
Enables:
Map-side joins
Sampling
Requires
CLUSTERED BY (id) INTO 32 BUCKETS;

7. File Formats
Row-Based

Text
CSV
JSON (slow)
Columnar (Preferred)
ORC (Hive optimized)
Parquet
ORC Advantages
Predicate pushdown
Compression
Indexes

ACID support

8. SerDe
What is SerDe
Serializer/Deserializer
Converts raw data ↔ Hive rows

Examples
LazySimpleSerDe
OpenCSVSerDe
JsonSerDe

9. Hive Query Optimization
Predicate Pushdown
Filters applied at file level
Column Pruning
Reads only required columns
Partition Pruning
Skips partitions
Cost Based Optimizer (CBO)
SET hive.cbo.enable=true;

🔟 Hive Execution Engines
MapReduce
Slow
Disk-heavy
Tez
DAG-based
Faster
Spark

In-memory

Best performance

11. Joins in Hive
Join Types

Inner
Left / Right / Full
Semi
Anti
Map-side Join
SET hive.auto.convert.join=true;

Skew Join
SET hive.optimize.skewjoin=true;

12. ACID & Transactions
Supported Tables

ORC
Bucketed
Operations
INSERT
UPDATE
DELETE
MERGE
Internals
Delta files
Compaction (minor/major)

13. Hive Locks
Shared locks
Exclusive locks
Managed via metastore

14. Security
Authorization
SQL Standard
Ranger / Sentry
Authentication
Kerberos

15. Hive vs Spark SQL (Interview Favorite)
Aspect	Hive	Spark SQL
Latency	High	Low
Engine	MR/Tez/Spark	In-memory
Use case	Batch DW	Interactive

16. Common Senior-Level Pitfalls

Over-partitioning
Small files
Skewed joins
Wrong file formats
No stats for CBO

17. Typical Senior Interview Questions

How does Hive avoid scanning full table?
How shuffle impacts performance?
When to use bucket vs partition?
ORC vs Parquet internals?
How ACID works internally?

✅ FINAL ADVICE

For senior interviews, always:

Explain internals
Mention trade-offs
Talk about performance
Compare with Spark