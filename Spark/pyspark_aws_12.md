"""****Start from here****"""
**AWS Glue (Spark)**
Best for: batch ETL, scheduled jobs, simple streaming, low-ops teams
You manage: almost nothing (serverless-ish); AWS manages infra
Scaling: automatic (Glue workers), quick to start, fewer cluster headaches
Strengths: easy to use, tight AWS integration, built-in data catalog, pay-per-use
Limitations: less control over JVM, node types, custom AMIs, deep tuning """

****>Amazon EMR (Clusters / EMR Serverless)****
Best for: heavy Spark workloads, tight tuning needs, custom libs, mixed engines (Spark/Presto/Hive), long-running streaming
You manage: cluster lifecycle + tuning (unless EMR Serverless)
Strengths: widest Spark control surface (instance types, EBS, spot, configs, bootstrap actions)
Limitations: more ops overhead, longer startup times (clusters), more complex pricing

Rule of thumb
If you want fast setup + minimal ops → Glue
If you want max performance control + complex workloads → EMR
If you want serverless feel but EMR Spark runtime → EMR Serverless"""

**Hands-on: Glue PySpark job (S3 CSV → transform → partitioned Parquet)**
Step 0: Prepare S3 folders
Example:
Input:  s3://my-bucket/raw/events/ (CSV with header, includes event_time)
Output: s3://my-bucket/curated/events_parquet/
Temp:   s3://my-bucket/glue-temp/

Step 1: Create an IAM role for Glue
Role needs, at minimum:
Read from input S3 prefix
Write to output S3 prefix
Write to temp S3 prefix
(If you use Glue Catalog/Athena later, add Glue permissions too.)

Step 2: Create the Glue Job (Console / Glue Studio)
Job type: Spark (not streaming)
Glue version: pick a modern one (e.g., Glue 4.0+; version controls Spark/Python)
IAM role: the one above
Job parameters (Default arguments) (examples):
--job-language = python
--TempDir = s3://my-bucket/glue-temp/ (Glue uses this for spills, some writes, etc.)
Custom:
--input_path = s3://my-bucket/raw/events/
--output_path = s3://my-bucket/curated/events_parquet/
(Optional) Bookmarks:
--job-bookmark-option = job-bookmark-enable (useful for incremental patterns; not mandatory)

***Glue Job Code**
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
# -----------------------------
# 1) Read job arguments
# -----------------------------
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "input_path", "output_path"]
    )
    input_path = args["input_path"]
    output_path = args["output_path"]


    # -----------------------------
    # 2) Initialize Glue + Spark
    # -----------------------------
    sc = SparkContext.getOrCreate()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session

    job = Job(glueContext)
    job.init(args["JOB_NAME"], args)


    # -----------------------------
    # 3) Read from S3 (CSV -> DataFrame)
    # -----------------------------
    raw = (
        spark.read
            .option("header", "true")
            .option("inferSchema", "false")  # keep deterministic; set true only for quick demos
            .csv(input_path)
    )

    # If event_time has a known pattern, specify it for correctness.
    # Example pattern: "yyyy-MM-dd HH:mm:ss"
    df = (
        raw
        .withColumn("event_time", F.to_timestamp(F.col("event_time")))  # or to_timestamp(col, "yyyy-MM-dd HH:mm:ss")
        .withColumn("dt", F.to_date(F.col("event_time")))
        .filter(F.col("dt").isNotNull())
    )

    # Reduce small files per partition-day:
    # - repartition("dt") clusters rows by dt and creates N partitions (depends on shuffle partitions)
    df = df.repartition("dt")


    # -----------------------------
    # 4) Write partitioned Parquet to S3
    # -----------------------------
    (
        df.write
        .mode("append")
        .format("parquet")
        .partitionBy("dt")
        .option("compression", "snappy")
        .save(output_path)
    )

    job.commit()


**With Json**
--events.json
{"event_time":"2026-01-18 10:10:01","user_id":"u1","action":"purchase","amount":499,"country":"IN","device":"android","metadata":{"ip":"1.2.3.4","campaign":"newyear"}}
{"event_time":"2026-01-18 10:10:15","user_id":"u2","action":"view","amount":0,"country":"IN","device":"ios","metadata":{"ip":"5.6.7.8","campaign":"brand"}}
{"event_time":"2026-01-18 10:11:02","user_id":"u1","action":"add_to_cart","amount":499,"country":"IN","device":"android","metadata":{"ip":"1.2.3.4","campaign":"newyear"}}
{"event_time":"2026-01-18 10:12:44","user_id":"u3","action":"purchase","amount":1299,"country":"SG","device":"web","metadata":{"ip":"9.9.9.9","campaign":"sale"}}
{"event_time":"2026-01-19 08:01:00","user_id":"u4","action":"view","amount":0,"country":"IN","device":"android","metadata":{"ip":"2.2.2.2","campaign":"push"}}

--simulate json files :
# generate_events_jsonl.py
import json
import os
import random
from datetime import datetime, timedelta

OUT_DIR = "data_raw_events"
os.makedirs(OUT_DIR, exist_ok=True)

users = ["u1", "u2", "u3", "u4", "u5"]
actions = ["view", "add_to_cart", "purchase"]
countries = ["IN", "SG", "US"]
devices = ["android", "ios", "web"]

start = datetime(2026, 1, 18, 10, 10, 0)

def make_event(i: int):
    ts = start + timedelta(seconds=i * random.randint(5, 25))
    action = random.choice(actions)
    amount = 0 if action != "purchase" else random.choice([199, 499, 1299, 2499])
    return {
        "event_time": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": random.choice(users),
        "action": action,
        "amount": amount,
        "country": random.choice(countries),
        "device": random.choice(devices),
        "metadata": {
            "ip": ".".join(str(random.randint(1, 255)) for _ in range(4)),
            "campaign": random.choice(["newyear", "brand", "sale", "push", "organic"])
        }
    }

# 1) single file
with open(os.path.join(OUT_DIR, "events_single.json"), "w", encoding="utf-8") as f:
    for i in range(200):
        f.write(json.dumps(make_event(i)) + "\n")

# 2) multiple files
for part in range(5):
    path = os.path.join(OUT_DIR, f"events_part_{part}.json")
    with open(path, "w", encoding="utf-8") as f:
        for i in range(100):
            f.write(json.dumps(make_event(part * 100 + i)) + "\n")

print(f"Created JSONL files under: {OUT_DIR}/")



**Glue json code**
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME", "input_path", "output_path"])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

input_path = args["input_path"]
output_path = args["output_path"]

# Read JSON Lines
raw = (
    spark.read
         .option("multiLine", "false")   # JSONL
         .json(input_path)
)

df = (
    raw
      .withColumn("event_time", F.to_timestamp("event_time", "yyyy-MM-dd HH:mm:ss"))
      .withColumn("dt", F.to_date("event_time"))
      .filter(F.col("dt").isNotNull())
)

# Optional: flatten nested struct for analytics friendliness
# df = df.withColumn("campaign", F.col("metadata.campaign")).drop("metadata")

# Reduce small files per dt
df = df.repartition("dt")

(
    df.write
      .mode("append")
      .format("parquet")
      .partitionBy("dt")
      .option("compression", "snappy")
      .save(output_path)
)

job.commit()


**Glue dynamic dataframe code**
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME", "input_path", "output_path"])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

input_path = args["input_path"]
output_path = args["output_path"]

# Read using DynamicFrame (handles schema drift better)
dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": [input_path],
        # "recurse": True,  # if needed for nested folders
    },
    format="json",
    format_options={
        "multiline": False  # JSONL
    }
)

# Convert to Spark DataFrame for complex transformations
df = dyf.toDF()

df = (
    df.withColumn("event_time", F.to_timestamp("event_time", "yyyy-MM-dd HH:mm:ss"))
      .withColumn("dt", F.to_date("event_time"))
      .filter(F.col("dt").isNotNull())
      .repartition("dt")
)

# Option 1: write using Spark (most common)
(df.write.mode("append")
   .format("parquet")
   .partitionBy("dt")
   .option("compression", "snappy")
   .save(output_path))

# Option 2 (optional): convert back to DynamicFrame if you want to use Glue sinks
# out_dyf = DynamicFrame.fromDF(df, glueContext, "out_dyf")

job.commit()


**EMR Code**:

from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("events-json-to-parquet").getOrCreate()

input_path = "s3://my-bucket/raw/events/"
output_path = "s3://my-bucket/curated/events_parquet/"

raw = spark.read.option("multiLine", "false").json(input_path)

df = (
    raw.withColumn("event_time", F.to_timestamp("event_time", "yyyy-MM-dd HH:mm:ss"))
       .withColumn("dt", F.to_date("event_time"))
       .filter(F.col("dt").isNotNull())
       .repartition("dt")
)

(df.write.mode("append")
   .format("parquet")
   .partitionBy("dt")
   .option("compression", "snappy")
   .save(output_path))

spark.stop()

