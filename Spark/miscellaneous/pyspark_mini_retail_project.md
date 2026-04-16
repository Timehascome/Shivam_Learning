from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum , avg, count, lit, to_date, to_timestamp, coalesce, round
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType, DateType
spark = SparkSession.builder \
    .appName("Mini Retail Project") \   
    .config("spark.sql.shuffle.partitions", "5") \
    .getOrCreate()
online_retail_schema = StructType([
    StructField("InvoiceNo", StringType(), True),
    StructField("StockCode", StringType(), True),
    StructField("Description", StringType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("InvoiceDate", StringType(), True),
    StructField("UnitPrice", DoubleType(), True),
    StructField("CustomerID", StringType(), True),
    StructField("Country", StringType(), True)
])
csv_file_path = "C:/Users/399sh/Downloads/Learning/Spark/retail_data/OnlineRetail.csv"
raw_orders_df = spark.read.schema(online_retail_schema).option("header", "true").option("inferSchema","false").csv(csv_file_path)
raw_orders_df.show(5, truncate=False)

processed_orders_df = raw_orders_df\
    .filter(col("Quantity")>0) \
    .filter(col("UnitPrice")>0) \
    .filter(col("CustomerId").isNotNull()) \
    .withColumn("Quantity", coalesce(col("Quantity"),lit(0)))\
    .withColumn("UnitPrice", coalesce(col("UnitPrice"),lit(0.0)))\
    .withColumn("InvoiceDate", to_timestamp(col("InvoiceDate"),"d/M/yyyy H:mm"))