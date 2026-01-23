A partition = chunk of data
1 partition → 1 task → 1 executor core
More partitions = more parallelism (up to cores)

spark.sparkContext.defaultParallelism   >> defines how many partitions Spark uses by default for ONLY RDDs when you don’t explicitly specify partitions.
spark.conf.get("spark.sql.shuffle.partitions")  >> This controls number of partitions created after a shuffle in Spark SQL / DataFrames / Datasets.
Source	    Default partitions
Local mode	number of CPU cores
HDFS / S3	based on file blocks
shuffle ops	spark.sql.shuffle.partitions (default 200)

# small data
spark.conf.set("spark.sql.shuffle.partitions", 10)
# medium job
spark.conf.set("spark.sql.shuffle.partitions", 50)
# large job
spark.conf.set("spark.sql.shuffle.partitions", executors * cores * 2)

Case 1: Reading from file systems (CSV / JSON / Parquet)
DataFrame default behaviour:
| Source   | Default behavior               |
| -------- | ------------------------------ |
| HDFS     | 1 partition ≈ 1 block (128 MB) |
| S3       | File splits (size-based)       |
| Local FS | File-split based               |
| Parquet  | Row-group based                |

>spark.sql.files.maxPartitionBytes   (default = 128 MB)  >> What controls split size?
 spark.sql.files.openCostInBytes     (default = 4 MB)   >> Spark uses openCostInBytes to prefer grouping many small files into one partition. Additional memeory added to each file to avoid small file issue and better partitioning

 >>Spark parallelism comes from splits, not file count.  Small file problem , cretes 100 partitions for 100 small files 

What is a Row Group in Parquet?
A row group is:
A horizontal chunk of rows
Stored independently
Designed for columnar reads
Parquet File
┌─────────────────────────┐
│ Row Group 1             │
│ ├── Column: id          │ → [1,2,3,4]
│ ├── Column: name        │ → [Alice,Bob,Charlie,David]
│ ├── Column: dept        │ → [Sales,HR,Sales,IT]
│ ├── Column: salary      │ → [1000,1500,2000,3000]
└─────────────────────────┘

CSV >> [1,Alice,Sales,1000][2,Bob,HR,1500][3,Charlie,Sales,2000]...

| Feature            | CSV / JSON  | Parquet   |
| ------------------ | ----------- | --------- |
| Partition unit     | File split  | Row group |
| Structure aware    | ❌ No        | ✅ Yes     |
| Predicate pushdown | ❌           | ✅         |
| Partition accuracy | Approximate | Precise   |
| Performance        | Slower      | Faster    |
==============================================================

Case 2: Reading from JDBC
Default: 1 partition ❌
Unless you specify:
partitionColumn  >> The column Spark uses to split the table into parallel ranges. Features : numeric/timestamp/uniform/indexed(very important)
[lowerBound, upperBound] >> Spark divides the range in equal chunks. Only used to calculate partition ranges. Range = upperBound - lowerBound
numPartitions  >> How many parallel JDBC connections / Spark tasks you want.
stride = (upperBound - lowerBound) / numPartitions
SELECT * FROM orders WHERE order_id >= 1 AND order_id < 100001
SELECT * FROM orders WHERE order_id >= 100001 AND order_id < 200001
...
Runs in parallel
Uses one DB connection
Produces one Spark partition

df = spark.read.jdbc(
    url=jdbc_url,
    table="orders",
    column="order_id",
    lowerBound=1,
    upperBound=1_000_000,
    numPartitions=10,
    properties=db_props
)
Task 1 → order_id 1–100000
Task 2 → order_id 100001–200000
...
Task 10 → order_id 900001–1000000

| Scenario         | Recommendation       |
| ---------------- | -------------------- |
| OLTP DB          | 4–8 partitions       |
| Large warehouse  | 8–16 partitions      |
| Weak DB          | Fewer partitions     |
| Time-based table | Use timestamp column |




==========================================================================
Case 3: DataFrame created in memory
df = spark.createDataFrame(data)
sparkContext.defaultParallelism
====================================================================
Case 4: After a shuffle (MOST IMPORTANT)
spark.sql.shuffle.partitions

Summary:
========
| Scenario            | Partition source             |
| ------------------- | ---------------------------- |
| Read from file      | File splits                  |
| Read from JDBC      | User-defined / 1             |
| Created from memory | defaultParallelism           |
| After shuffle       | spark.sql.shuffle.partitions |


*******ABOVE All about partitions*******************

What is a Shuffle?
Data movement across executors via disk + network.

Operations that cause shuffle:
groupBy
reduceByKey
join
distinct
orderBy
repartition

Why are shuffles expensive?
Because Spark must:
Write intermediate data to disk
Transfer data over the network
Read data back on another executor
Deserialize & aggregate
>Most Spark performance issues come from shuffles.

How to Reduce Shuffle Cost?
spark.conf.set("spark.sql.shuffle.partitions", 50).
Filter before join.
Broadcast small tables.
Use reduceByKey instead of groupByKey.
Avoid unnecessary repartition.
Partition on join keys.


Join strategies to reduce shuffle:
Broadcast join  >> spark.sql.autoBroadcastJoinThreshold allows it>> “Send small table everywhere → join locally”
Sort-merge join  >> Default & most common for large ↔ large >> sort both tables merge like zipper [Algo >> merge sort]
Shuffle hash join >> Faster than SMJ but memory-sensitive >> One table is much smaller than the other >> Shuffle BOTH tables by join key>> Build hash table (on smaller side)>>Probe with large table >> If hash table doesn’t fit → OOM
Example:
Employees (Large)
Departments (Small / Medium)

| Join Type    | Shuffle   | Sort  | Memory | Speed   | Use Case       |
| ------------ | -------   | ----  | ------ | ------- | -------------- |
| Sort-Merge   | ✅       | ✅    | Medium | Medium  | Large ↔ Large  |
| Shuffle Hash | ✅       | ❌    | High   | Fast    | Medium ↔ Large |
| Broadcast    | ❌       | ❌    | Low    | Fastest | Small ↔ Large  |






