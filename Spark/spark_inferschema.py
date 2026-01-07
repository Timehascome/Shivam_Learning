# we see that inferSchema option infers the correct data types for each column in the CSV file.
#inferschema creates a job to scan the data and determine the data types.

df_csv = spark.read.option("header", True).option("inferSchema", True).csv(r"C:\Users\399sh\Downloads\Learning\Spark\iris.csv")
df_csv.show(5, truncate=False)
+------------+-----------+------------+-----------+-------+
|sepal.length|sepal.width|petal.length|petal.width|variety|
+------------+-----------+------------+-----------+-------+
|5.1         |3.5        |1.4         |0.2        |Setosa |
|4.9         |3.0        |1.4         |0.2        |Setosa |
|4.7         |3.2        |1.3         |0.2        |Setosa |
|4.6         |3.1        |1.5         |0.2        |Setosa |
|5.0         |3.6        |1.4         |0.2        |Setosa |
+------------+-----------+------------+-----------+-------+
only showing top 5 rows

df_csv.printSchema()
root
 |-- sepal.length: double (nullable = true)
 |-- sepal.width: double (nullable = true)
 |-- petal.length: double (nullable = true)
 |-- petal.width: double (nullable = true)
 |-- variety: string (nullable = true).

# Without inferSchema option, all columns are read as strings by default.

>>> df_csv = spark.read.option("header", True).csv(r"C:\Users\399sh\Downloads\Learning\Spark\iris.csv")
>>> df_csv.show(5, truncate=False)
+------------+-----------+------------+-----------+-------+
|sepal.length|sepal.width|petal.length|petal.width|variety|
+------------+-----------+------------+-----------+-------+
|5.1         |3.5        |1.4         |.2         |Setosa |
|4.9         |3          |1.4         |.2         |Setosa |
|4.7         |3.2        |1.3         |.2         |Setosa |
|4.6         |3.1        |1.5         |.2         |Setosa |
|5           |3.6        |1.4         |.2         |Setosa |
+------------+-----------+------------+-----------+-------+
only showing top 5 rows

>>> df_csv.printSchema()
root
 |-- sepal.length: string (nullable = true)
 |-- sepal.width: string (nullable = true)
 |-- petal.length: string (nullable = true)
 |-- petal.width: string (nullable = true)
 |-- variety: string (nullable = true)


 #inferSchema is relevant only for CSV.JSON always infers schema from data, and Parquet never infers schema because it stores schema in metadata.