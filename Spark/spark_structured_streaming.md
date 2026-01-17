1) Mental Model
Structured Streaming is basically:
>A continuously running query
>Treating stream data as an unbounded table
>Executed in micro-batches (default) or continuous mode (rare)
>Uses checkpointing to remember progress and state
**Key terms :**
>>Source (where data comes from)
>>Sink (where results go)
>>Trigger (when to run batches) **
> when spark should wake up and run the job.
| Trigger                        | Meaning                           |
| ------------------------------ | --------------------------------- |
| `processingTime("10 seconds")` | Run every 10 seconds              |
| `once()`                       | Run once & stop                   |
| `availableNow()`               | Process all available data & stop |
| default                        | As fast as possible               |

>>Output mode (append, update, complete)**
>what results are written.
| Mode         | Meaning             | Used when        |
| ------------ | ------------------- | ---------------- |
| **append**   | Only new rows       | No updates later |
| **update**   | Only changed rows   | Aggregations     |
| **complete** | Entire result table | Small datasets   |

>>State (for aggregations, joins, dedup) **  >> stored intermediate results across batches >> memory of past batches
| Operation     | State needed? |
| ------------- | ------------- |
| Aggregations  | ✅             |
| Joins         | ✅             |
| Deduplication | ✅             |
| Simple select | ❌             |

>>Watermark (late data handling) **  >> Watermark = expiry date for events
>.withWatermark("event_time", "30 minutes")
“I’ll accept data up to 30 minutes late.Older than that → drop it.”

>>Checkpoint location (fault tolerance) **
>Checkpoint = Spark’s recovery brain
Stored on:
HDFS
S3
ADLS
.option("checkpointLocation", "/spark/checkpoints/orders")
What is saved?
✔️ Kafka offsets
✔️ State (aggregations, joins)
✔️ Batch progress
Failure scenario
Spark crashes at batch 25
Restart job
Spark:
Reads checkpoint
Resumes from batch 26
No data loss / duplication
**Full working example**
query = (
    orders_df
    .withWatermark("event_time", "30 minutes")
    .groupBy("product")
    .sum("amount")
    .writeStream
    .outputMode("update")
    .trigger(processingTime="10 minutes")
    .option("checkpointLocation", "/spark/checkpoints/orders")
    .format("console")
    .start()
)

| Concept     | One-liner                |
| ----------- | ------------------------ |
| Trigger     | When micro-batches run   |
| Output mode | What results are written |
| State       | Stored intermediate data |
| Watermark   | Late data cutoff         |
| Checkpoint  | Fault-tolerant recovery  |

2) Hello Streaming (simple)
**Lab 1**: “rate” source + console sink:

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (SparkSession.builder
         .appName("ss_rate_demo")
         .master("local[*]")
         .getOrCreate())

df = spark.readStream.format("rate").option("rowsPerSecond", 5).load()
out = df.select(col("timestamp"), col("value"))

q = (out.writeStream
     .format("console")
     .outputMode("append")
     .option("truncate", "false")
     .start())

q.awaitTermination()

Concepts you learn:
streaming DataFrame
readStream / writeStream
outputMode

**Lab2** : File stream + schema (realistic ingestion)
Stream JSON/CSV files from a directory
Create folder: data/in/ and data/chk/
==
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import *

schema = StructType([
    StructField("event_time", StringType()),
    StructField("user_id", StringType()),
    StructField("action", StringType()),
    StructField("amount", IntegerType()),
])

raw = (spark.readStream
       .schema(schema)
       .option("maxFilesPerTrigger", 1)
       .json("data/in"))

events = raw.withColumn("event_time", to_timestamp("event_time"))

q = (events.writeStream
     .format("console")
     .outputMode("append")
     .option("checkpointLocation", "data/chk/file_ingest")
     .start())
q.awaitTermination()

Concepts you learn: 
schema is mandatory for file streaming
checkpointing
maxFilesPerTrigger