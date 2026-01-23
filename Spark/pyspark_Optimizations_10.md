**Adaptive Query Execution (AQE) (Concept → UI → Behavior):**
>What AQE actually does?

Before AQE
Query plan is fixed before execution
Optimizer guesses:
Join strategy
Shuffle partitions
Broadcast size

With AQE
Spark re-optimizes during execution based on real stats.
AQE can:
Switch SortMergeJoin → BroadcastJoin
Coalesce shuffle partitions
Split skewed partitions
Reduce unnecessary shuffles

Configs:
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "50MB")

HandsOn:
from pyspark.sql.functions import *
fact = spark.range(0, 10_000_000).withColumn("key", col("id") % 100)
dim = spark.range(0, 100).withColumn("key", col("id"))
fact.show(5)
dim.show(5)
result = fact.join(dim, "key").groupBy("key").count()
result.explain("formatted")
result.count()

Check Spark UI → SQL → Physical Plan
Look for:
AdaptiveSparkPlan
BroadcastHashJoin appearing after execution
>Initial plan vs Final plan
>Reduced shuffle partitions
>Shorter stage execution

**What is skew?**
Skew = uneven data distribution
country = IN → 70% data
country = US → 5%
others → rest
1 task runs forever
Other executors idle
OOM / timeout
**df.groupBy("key").count().orderBy(desc("count")).show()**
Spark UI:
One task much longer
Shuffle read/write imbalance
spark.sql.adaptive.skewJoin.enabled = true

>Detects large partitions
>Splits skewed partitions
>Runs them in parallel

When AQE is NOT enough (20 min)
❌ Extreme skew
❌ Old Spark versions
❌ Custom aggregations

**Salting Technique (Manual but Powerful)**
Fix skew deterministically.
You artificially spread hot keys
Example:
from pyspark.sql.functions import rand, floor, concat
salt_range = 10
fact_salted = fact.withColumn(
    "salt", floor(rand() * salt_range)
).withColumn(
    "salted_key", concat(col("key"), lit("_"), col("salt"))
)
dim_salted = dim.crossJoin(
    spark.range(0, salt_range).withColumnRenamed("id", "salt")
).withColumn(
    "salted_key", concat(col("key"), lit("_"), col("salt"))
)
joined = fact_salted.join(dim_salted, "salted_key")

| Scenario       | Solution               |
| -------------- | ---------------------- |
| Small skew     | AQE                    |
| Join skew      | AQE skew join          |
| Extreme skew   | Salting                |
| Known hot keys | Filter + separate path |

**Give Spark Optimization techniques:**
1) Partitioning and paralleslism
Default partitions (file-based, JDBC, shuffle)
repartition() vs coalesce()
spark.sql.shuffle.partitions
spark.sql.files.maxPartitionBytes
2) Join Optimization
Broadcast Hash Join
Shuffle Hash Join
Sort Merge Join
3) Filter & Projection Pushdown
Pushes filters to data source
Reads only required columns
Supported for parquet and ORC
4) Caching & Persistence
MEMORY_ONLY
MEMORY_AND_DISK
DISK_ONLY
Cache only reused DataFrames\
Unpersist aggressively
Never cache raw data blindly
5) File Size Optimization
repartition() before write
spark.sql.files.maxRecordsPerFile
Compaction jobs (Delta/Iceberg)
6) Serialization & Tungsten
Off-heap memory
Binary processing
Code generation
spark.serializer=org.apache.spark.serializer.KryoSerializer
7) Shuffle Optimization
Costly operations
groupBy
distinct
join
Reduce shuffle data
Use reduceByKey (RDD)
Tune spark.sql.shuffle.partitions
8) Data Skipping & Z-Ordering
Skips entire files
Faster selective queries
OPTIMIZE table ZORDER BY (user_id, date)
9) Bucketing
Repeated joins on same key
Works best with Hive tables
Less flexible than partitioning
10) Executor & Cluster Sizing
CPU vs memory bound jobs
Executor count vs core count
Avoid GC pressure
11) GC & OOM Optimization
Wide transformations
Large cached DataFrames
Skew
12) Reading from JDBC
.option("partitionColumn", "id") \
.option("lowerBound", 1) \
.option("upperBound", 1_000_000) \
.option("numPartitions", 50)
13) WholeStageCodeGen
Fuses operators
Reduces virtual calls
Improves CPU efficiency
14) Cost-Based Optimizer (CBO)
spark.sql.cbo.enabled=true
spark.sql.statistics.histogram.enabled=true
15) AQE + CBO synergy
CBO → better initial plan
AQE → runtime correction

Memory points:
=============
DATA SIZE      → Partitioning, File size
DATA SHAPE     → Skew, Salting, Bucketing
DATA FORMAT    → Parquet, Pushdown, Z-order
DATA FLOW      → Join strategy, Shuffle
MEMORY         → Cache, GC, Tungsten
RUNTIME        → AQE, CBO
