



iwr "https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv" -OutFile "C:Users399shDownloadsLearningSparkiris.csv"

iwr "https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json" -OutFile "C:Users399shDownloadsLearningSparkdummy.json"

iwr "https://www.timestored.com/data/sample/iris.parquet" -OutFile "C:Users399shDownloadsLearningSparkiris.parquet"



from pyspark.sql import SparkSession

from pyspark.sql import functions as F

from pyspark.sql.types import DoubleType, StringType



spark = SparkSession.builder.appName("ReadFiles").getOrCreate()



# CSV

df_csv = spark.read.option("header", True).option("inferSchema", True).csv(r"C:Users399shDownloadsLearningSparkiris.csv")

df_csv.show(5, truncate=False)

df_csv.printSchema()



# JSON (this file is a JSON array; spark can read it)

df_json = spark.read.option("multiline", True).json(r"C:Users399shDownloadsLearningSparkdummy.json")

df_json.show(5, truncate=False)

df_json.printSchema()



# Parquet

df_parquet = spark.read.parquet(r"C:Users399shDownloadsLearningSparkiris.parquet")

df_parquet.show(5, truncate=False)

df_parquet.printSchema()



#select 



*df_csv.select(*

    *F.col("sepal.length").alias("sepal_length"),*

    *F.col("variety")*

*).show(5)*



#filter /where



df_csv.filter(F.col("variety") == "Setosa").show(5)



#withColumn



df2 = df_csv.withColumn("sepal_length_x2", F.col("sepal.length") * 2)

df2.show(5)



#when/otherwise



df3 = df_csv.withColumn(

&nbsp;   "size_bucket",

&nbsp;   F.when(F.col("petal.length") >= 5.0, F.lit("large"))

&nbsp;    .when(F.col("petal.length") >= 3.0, F.lit("medium"))

&nbsp;    .otherwise(F.lit("small"))

)

df3.select("petal.length", "size_bucket").show(10)





#cast

&nbsp;

df4 = df_csv.withColumn("sepal_len_d", F.col("sepal.length").cast("double"))

df4.printSchema()



#Datefunctions



raw = spark.createDataFrame(

&nbsp;   [("2026-01-06", "10", None),

&nbsp;    ("2026-01-05", "3",  "7")],

&nbsp;   ["dt_str", "qty_str", "price_str"]

)



clean = (raw

&nbsp;   .withColumn("dt", F.to_date("dt_str", "yyyy-MM-dd"))

&nbsp;   .withColumn("year", F.year("dt"))

&nbsp;   .withColumn("month", F.month("dt"))

&nbsp;   .withColumn("qty", F.col("qty_str").cast("int"))

&nbsp;   .withColumn("price", F.col("price_str").cast("double"))

)



clean.show()

clean.printSchema()



#Null Handling



df_clean = (raw

&nbsp;   # cast first

&nbsp;   .withColumn("qty", F.col("qty_str").cast("int"))

&nbsp;   .withColumn("price", F.col("price_str").cast("double"))



&nbsp;   # null handling: replace null price with 0.0

&nbsp;   .fillna({"price": 0.0})



&nbsp;   # derived column: total = qty * price (handle null qty too)

&nbsp;   .withColumn("qty_nn", F.coalesce(F.col("qty"), F.lit(0)))

&nbsp;   .withColumn("total", F.col("qty_nn") * F.col("price"))



&nbsp;   # when/otherwise for flags

&nbsp;   .withColumn(

&nbsp;       "is_free",

&nbsp;       F.when(F.col("price") == 0.0, F.lit(1)).otherwise(F.lit(0))

&nbsp;   )

)



df_clean.show()

df_clean.printSchema()





#) Type casting checklist (for interviews + real jobs)



IDs → string



amounts → decimal(18,2) or double (prefer decimal for money)



dates → date / timestamps → timestamp



booleans → boolean

























