#pyspark group by aggregations examples
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum, max, min        
spark = SparkSession.builder.appName("Spark GroupBy Aggregations").getOrCreate()
data = [("Alice", "Sales", 5000),
        ("Bob", "Sales", 6000),             
        ("Charlie", "HR", 5500),
        ("David", "HR", 7000),
        ("Eve", "IT", 8000),
        ("Frank", "IT", 7500),
        ("Grace", "Sales", 6500)]
columns = ["Name", "Department", "Salary"]
df = spark.createDataFrame(data, columns)                   
df.show()
# Group by Department and calculate average salary          
df.groupBy("Department").agg(avg("Salary").alias("Avg_Salary")).show()
# Group by Department and calculate total salary    
df.groupBy("Department").agg(sum("Salary").alias("Total_Salary")).show()    
# Group by Department and count number of employees 
df.groupBy("Department").agg(count("Name").alias("Employee_Count")).show()
# Group by Department and find maximum salary   
df.groupBy("Department").agg(max("Salary").alias("Max_Salary")).show()
# Group by Department and find minimum salary
df.groupBy("Department").agg(min("Salary").alias("Min_Salary")).show()
# Multiple aggregations: average and total salary per department
df.groupBy("Department").agg(
    avg("Salary").alias("Avg_Salary"),
    sum("Salary").alias("Total_Salary")
).show()    
# Stop the Spark session
spark.stop()
+-------+-----------+
|   name| department|
+-------+-----------+
|  ALice|      Sales|   
|    Bob|         HR|
|Charlie|Engineering|
|  David|  Marketing|
|  Frank|      Sales|
+-------+-----------+
+---+-------+
| id|   city|
+---+-------+
|  1|NewYork|
|  3| London|
|  5|  Paris|
|  1|     SF|
+---+-------+   



>>> df.show()
+-------+----------+------+
|   Name|Department|Salary|
+-------+----------+------+
|  Alice|     Sales|  5000|
|    Bob|     Sales|  6000|
|Charlie|        HR|  5500|
|  David|        HR|  7000|
|    Eve|        IT|  8000|
|  Frank|        IT|  7500|
|  Grace|     Sales|  6500|
+-------+----------+------+
#get me employee with max salary
df.orderBy(col("Salary").desc()).limit(1).show()

+-------+----------+------+
|   Name|Department|Salary|
+-------+----------+------+
|    Eve|        IT|  8000|
+-------+----------+------+


#import collect_list and collect_set
from pyspark.sql.functions import collect_list, collect_set
>>> df.groupBy(col("Department")).agg(collect_list("Name").alias("employee_list")).show()
+----------+-------------------+
|Department|      employee_list|
+----------+-------------------+
|     Sales|[Alice, Bob, Grace]|
|        HR|   [Charlie, David]|
|        IT|       [Eve, Frank]|
+----------+-------------------+

>>> df.groupBy(col("Department")).agg(collect_set("Name").alias("employee_list")).show()
+----------+-------------------+
|Department|      employee_list|
+----------+-------------------+
|     Sales|[Grace, Bob, Alice]|
|        HR|   [David, Charlie]|
|        IT|       [Frank, Eve]|
+----------+-------------------+




>>> df.groupBy("Department").agg(sum(when(col("Salary")==7000, 1)).alias("con_count")).show()
+----------+---------+
|Department|con_count|
+----------+---------+
|     Sales|     NULL|
|        HR|        1|
|        IT|     NULL|
+----------+---------+

>>> df.groupBy("Department").agg(count(when(col("Salary")==7000, "NULL")).alias("con_count")).show()
+----------+---------+
|Department|con_count|
+----------+---------+
|     Sales|        0|
|        HR|        1|
|        IT|        0|
+----------+---------+

>>> df.show()
+-------+----------+------+
|   Name|Department|Salary|
+-------+----------+------+
|  Alice|     Sales|  5000|
|    Bob|     Sales|  6000|
|Charlie|        HR|  5500|
|  David|        HR|  7000|
|    Eve|        IT|  8000|
|  Frank|        IT|  7500|
|  Grace|     Sales|  6500|
+-------+----------+------+

>>> df.groupBy(col("Name")).pivot("Department").sum("Salary").show()
+-------+----+----+-----+
|   Name|  HR|  IT|Sales|
+-------+----+----+-----+
|  Grace|NULL|NULL| 6500|
|Charlie|5500|NULL| NULL|
|    Bob|NULL|NULL| 6000|
|  Alice|NULL|NULL| 5000|
|    Eve|NULL|8000| NULL|
|  David|7000|NULL| NULL|
|  Frank|NULL|7500| NULL|
+-------+----+----+-----+

>>> df.groupBy(col("Name")).pivot("Department").sum("Salary").fillna(0).show()
+-------+----+----+-----+
|   Name|  HR|  IT|Sales|
+-------+----+----+-----+
|  Grace|   0|   0| 6500|
|Charlie|5500|   0|    0|
|    Bob|   0|   0| 6000|
|  Alice|   0|   0| 5000|
|    Eve|   0|8000|    0|
|  David|7000|   0|    0|
|  Frank|   0|7500|    0|
+-------+----+----+-----+

