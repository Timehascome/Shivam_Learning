# Practice:
# select
# withColumn
# drop
# withColumnRenamed
# filter / where
# handling nulls
# trim / spaces
# length
# cast
# when / otherwise

#Data set used will be instacart online grocery delivery data set
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\orders.csv and 
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\order_products__prior.csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, length, trim   
spark = SparkSession.builder.appName("Transformations").getOrCreate()
# Load the orders data
orders_df = spark.read.csv("C:\\Users\\399sh\\Desktop\\git\\Shivam_Learning\\Spark\\int_probs\\archive\\orders.csv", header=True, inferSchema=True)
# Load the order products data
order_products_df = spark.read.csv("C:\\Users\\399sh\\Desktop\\git\\Shivam_Learning\\Spark\\int_probs\\archive\\order_products__prior.csv", header=True, inferSchema=True)
# Select specific columns from orders_df
# Select only order_id, user_id, and order_number from orders_df
selected_orders_df = orders_df.select("order_id", "user_id", "order_number")
# Add a new column to orders_df that categorizes orders as 'First Order' or 'Repeat Order'
orders_with_category_df = orders_df.withColumn("order_category", when(col("order_number") == 1, "First Order").otherwise("Repeat Order"))
# Drop the 'eval_set' column from orders_df as it's not needed for analysis
orders_dropped_df = orders_df.drop("eval_set")      
# Rename the 'order_number' column to 'order_count' in orders_df for better clarity
orders_renamed_df = orders_df.withColumnRenamed("order_number", "order_count")
# Filter orders_df to include only orders where the order_number is greater than 5  
#   Filter orders to include only those with more than 5 items in the order
filtered_orders_df = orders_df.filter(col("order_number") > 5)  
# Handle null values in the 'days_since_prior_order' column by filling them with 0
orders_filled_df = orders_df.fillna({"days_since_prior_order": 0})      
# Trim leading and trailing spaces from the 'order_category' column in orders_with_category_df
orders_trimmed_df = orders_with_category_df.withColumn("order_category", trim(col("order_category")))
# Calculate the length of the 'order_category' column and create a new column 'category_length'
orders_length_df = orders_with_category_df.withColumn("category_length", length(col("order_category")))
# Cast the 'order_number' column to string type in orders_df    
# Cast the 'order_number' column to string type for better readability
orders_casted_df = orders_df.withColumn("order_number_str", col("order_number").cast("string"))
# Use when/otherwise to create a new column 'order_type' that categorizes orders as 'High Value' if the order_number is greater than 10, and 'Low Value' otherwise
orders_type_df = orders_df.withColumn("order_type", when(col("order_number") > 10, "High Value").otherwise("Low Value"))
# Show the resulting DataFrames to verify the transformations
print("Selected Orders DataFrame:") 
selected_orders_df.show(5)
print("Orders with Category DataFrame:")    
orders_with_category_df.show(5)
print("Orders with Dropped Column DataFrame:")  
orders_dropped_df.show(5)
print("Orders with Renamed Column DataFrame:")  
orders_renamed_df.show(5)
print("Filtered Orders DataFrame:")
filtered_orders_df.show(5)
print("Orders with Filled Nulls DataFrame:")
orders_filled_df.show(5)
print("Orders with Trimmed Category DataFrame:")
orders_trimmed_df.show(5)
print("Orders with Category Length DataFrame:")
orders_length_df.show(5)
print("Orders with Casted Order Number DataFrame:") 
orders_casted_df.show(5)
print("Orders with Order Type DataFrame:")
orders_type_df.show(5)      
        