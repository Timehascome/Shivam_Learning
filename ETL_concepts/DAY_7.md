Concepts:
Full load vs incremental load
Watermarks
Change Data Capture (CDC)
Delete handling
Hands-on
SQL incremental load using last_updated_ts
************************************************************************
PySpark CDC simulation:
Inserts
Updates
Deletes
***************
from pyspark.sql import functions as F
# Target (existing)
current_df = spark.createDataFrame([
    (1, "Asha", "BLR", 100),
    (2, "Ravi", "HYD", 200),
    (3, "Neha", "DEL", 300),
    (5, "Kiran","MUM", 500),
], ["id", "name", "city", "salary"])

# Incoming (today)
incoming_df = spark.createDataFrame([
    (1, "Asha", "BLR", 100),   # unchanged
    (2, "Ravi", "HYD", 250),   # update (salary changed)
    (4, "Manu", "PUN", 400),   # insert (new id)
    (5, "Kiran","MUM", 500),   # unchanged
    # id=3 missing => delete
], ["id", "name", "city", "salary"])

inserts_df = (
    incoming_df.alias("n")
    .join(current_df.select("id").alias("c"), on="id", how="left_anti")
    .withColumn("cdc_op", F.lit("I"))
)

deletes_df = (
    current_df.alias("c")
    .join(incoming_df.select("id").alias("n"), on="id", how="left_anti")
    .withColumn("cdc_op", F.lit("D"))
)

non_key_cols = ["name", "city", "salary"]

def row_hash(df, cols, alias):
    # coalesce to stable strings to avoid null issues
    exprs = [F.coalesce(F.col(c).cast("string"), F.lit("∅")) for c in cols]
    return df.select(
        "id",
        F.sha2(F.concat_ws("||", *exprs), 256).alias(f"{alias}_hash"),
        *[F.col(c).alias(f"{alias}_{c}") for c in cols]
    )

cur_h = row_hash(current_df, non_key_cols, "c")
new_h = row_hash(incoming_df, non_key_cols, "n")

updates_df = (
    new_h.join(cur_h, on="id", how="inner")
    .filter(F.col("n_hash") != F.col("c_hash"))
    .select(
        "id",
        *[F.col(f"n_{c}").alias(c) for c in non_key_cols]
    )
    .withColumn("cdc_op", F.lit("U"))
)

cdc_df = inserts_df.select("id","name","city","salary","cdc_op") \
    .unionByName(updates_df.select("id","name","city","salary","cdc_op")) \
    .unionByName(deletes_df.select("id","name","city","salary","cdc_op"))

cdc_df.orderBy("id").show(truncate=False)

# start from current, remove deletes and to-be-updated keys
keys_to_delete = deletes_df.select("id")
keys_to_update = updates_df.select("id")

base_df = current_df \
    .join(keys_to_delete, on="id", how="left_anti") \
    .join(keys_to_update, on="id", how="left_anti")

new_target_df = base_df \
    .unionByName(inserts_df.drop("cdc_op")) \
    .unionByName(updates_df.drop("cdc_op"))

new_target_df.orderBy("id").show(truncate=False)


>>Inserts: left_anti from new → current
Deletes: left_anti from current → new
Updates: join on key + compare hash of non-key columns (null-safe)
This simulates CDC even without real log-based CDC tools.
