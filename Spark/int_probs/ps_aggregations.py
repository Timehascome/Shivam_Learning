# Phase 2: Aggregations
# Once rows are cleaned, aggregate them.
# Practice:
# groupBy
# count
# avg
# sum
# min / max
# countDistinct
# multiple aggregations together
# having-like filtering after aggregation
#Data set used will be instacart online grocery delivery data set
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\orders.csv and 
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\order_products__prior.csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, min, max, countDistinct
spark = SparkSession.builder.appName("Aggregations").getOrCreate()  
# Load the orders data
orders_df = spark.read.csv("C:\\Users\\399sh\\Desktop\\git\\Shivam_Learning\\Spark\\int_probs\\archive\\orders.csv", header=True, inferSchema=True)
# Load the order products data      
order_products_df = spark.read.csv("C:\\Users\\399sh\\Desktop\\git\\Shivam_Learning\\Spark\\int_probs\\archive\\order_products__prior.csv", header=True, inferSchema=True)
# Group by user_id and count the number of orders for each user
orders_count_df = orders_df.groupBy("user_id").agg(count("order_id").alias("total_orders"))
# Group by user_id and calculate the average order_number for each user
orders_avg_df = orders_df.groupBy("user_id").agg(avg("order_number").alias("average_order_number"))
# Group by user_id and calculate the total sum of order_number for each user    orders_sum_df = orders_df.groupBy("user_id").agg(sum("order_number").alias("total_order_number"))
orders_sum_df = orders_df.groupBy("user_id").agg(sum("order_number").alias("total_order_number"))
# Group by user_id and calculate the minimum and maximum order_number for each user 
orders_min_max_df = orders_df.groupBy("user_id").agg(min("order_number").alias("min_order_number"), max("order_number").alias("max_order_number"))
# Group by user_id and count the distinct number of order_number for each user  
orders_distinct_count_df = orders_df.groupBy("user_id").agg(countDistinct("order_number").alias("distinct_order_count"))
# Group by user_id and calculate multiple aggregations together (count, avg, sum)
orders_multiple_agg_df = orders_df.groupBy("user_id").agg(count("order_id").alias("total_orders"), avg("order_number").alias("average_order_number"), sum("order_number").alias("total_order_number"))
# Group by user_id and filter users who have more than 5 total orders (having-like filtering)
orders_having_df = orders_count_df.filter(col("total_orders") > 5)  
# Show the resulting DataFrames to verify the aggregations
print("Orders Count DataFrame:")        
orders_count_df.show(5)
print("Orders Average DataFrame:")  
orders_avg_df.show(5)
print("Orders Sum DataFrame:")  
orders_sum_df.show(5)   
print("Orders Min and Max DataFrame:")
orders_min_max_df.show(5)
print("Orders Distinct Count DataFrame:")
orders_distinct_count_df.show(5)    
print("Orders Multiple Aggregations DataFrame:")
orders_multiple_agg_df.show(5)
print("Orders Having-like Filtering DataFrame:")
orders_having_df.show(5)
