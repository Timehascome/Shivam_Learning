from pyspark.sql import SparkSession, functions as F

spark = (
    SparkSession.builder
    .appName("SparkUI-Demo-Shuffle-Skew")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "200")
    .config("spark.default.parallelism", "200")
    .config("spark.sql.autoBroadcastJoinThreshold", "-1")
    .config("spark.ui.enabled", "true")
    .config("spark.sql.adaptive.enabled", "false")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")
print("Spark UI:", spark.sparkContext.uiWebUrl)

N = 8_000_000
fact = (
    spark.range(0, N)
    .withColumn(
        "key",
        F.when(F.rand(seed=42) < F.lit(0.90), F.lit(0))
         .otherwise((F.col("id") % 1000).cast("int"))
    )
    .withColumn("v1", (F.col("id") % 1000).cast("int"))
    .withColumn("v2", (F.col("id") * 3 % 1000).cast("int"))
    .repartition(200, "key")
)

dim = (
    spark.range(0, 1000)
    .withColumnRenamed("id", "key")
    .withColumn("dim_value", F.concat(F.lit("K_"), F.col("key").cast("string")))
    .repartition(50, "key")
)

joined = fact.join(dim, on="key", how="inner")

agg = (
    joined.groupBy("key", "dim_value")
    .agg(
        F.count("*").alias("cnt"),
        F.sum("v1").alias("sum_v1"),
        F.avg("v2").alias("avg_v2"),
    )
    .orderBy(F.desc("cnt"))
)

agg_cached = agg.cache()

print("Running actions now...")
agg_cached.limit(20).explain("formatted")
top20 = agg_cached.limit(20).collect()

print("Top 5 rows:", top20[:5])

total_keys = agg_cached.count()
print("Total aggregated rows:", total_keys)


print("\nDONE. Keep Spark UI open. Press Enter to stop the Spark application...")
input()

spark.stop()
