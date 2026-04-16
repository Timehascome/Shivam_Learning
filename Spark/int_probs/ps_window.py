#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\orders.csv 
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\order_products__prior.csv
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\order_products__train.csv
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\aisles.csv 
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\products.csv

# Practice:
# row_number
# rank
# dense_rank
# lag
# lead
# running sum
# partitionBy
# orderBy
# rowsBetween
# Goal:
# Learn when window is better than groupBy.

from pyspark.sql import SparkSession
from pyspark.sql import functions as F  
from pyspark.sql.window import Window   
spark = SparkSession.builder.appName("window").getOrCreate()
orders = spark.read.csv("C:\\Users\\399sh\\Desktop\\git\\Shivam_Learning\\Spark\\int_probs\\archive\\orders.csv", header=True, inferSchema=True)
orders.show(5)
orders.printSchema()
orders.groupBy("user_id").count().show(5)       
orders.withColumn("row_number", F.row_number().over(Window.partitionBy("user_id").orderBy("order_number"))).show(5)
orders.withColumn("rank", F.rank().over(Window.partitionBy("user_id").orderBy("order_number"))).show(5)
orders.withColumn("dense_rank", F.dense_rank().over(Window.partitionBy("user_id").orderBy("order_number"))).show(5)
orders.withColumn("lag", F.lag("order_number").over(Window.partitionBy("user_id").orderBy("order_number"))).show(5)
orders.withColumn("lead", F.lead("order_number").over(Window.partitionBy("user_id").orderBy("order_number"))).show(5)
orders.withColumn("running_sum", F.sum("order_number").over(Window.partitionBy("user_id").orderBy("order_number").rowsBetween(Window.unboundedPreceding, Window.currentRow))).show(5)   
        