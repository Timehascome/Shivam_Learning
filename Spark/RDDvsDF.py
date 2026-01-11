>>> emp_data = [
...     (1, "Alice", "Sales", 1000, "sql,spark"),
...     (2, "Bob", "Sales", 1500, "python,spark"),
...     (3, "Charlie", "HR", 1200, "sql"),
...     (4, "David", "HR", 2000, "python,aws")
... ]
>>> emp_data = [
...     (1, "Alice", "Sales", 1000, "sql,spark"),
...     (2, "Bob", "Sales", 1500, "python,spark"),
...     (3, "Charlie", "HR", 1200, "sql"),
...     (4, "David", "HR", 2000, "python,aws")
... ]
>>> dept_data = [
...     ("Sales", "NY"),
...     ("HR", "BLR")
... ]
>>> df_emp  = spark.createDataFrame(emp_data, ["id", "name", "dept", "salary", "skills"])
>>> df_dept = spark.createDataFrame(dept_data, ["dept", "city"])
>>> rdd_emp  = spark.sparkContext.parallelize(emp_data)
>>> rdd_dept = spark.sparkContext.parallelize(dept_data)
>>> df_emp.show(truncate=False)
+---+-------+-----+------+------------+
|id |name   |dept |salary|skills      |
+---+-------+-----+------+------------+
|1  |Alice  |Sales|1000  |sql,spark   |
|2  |Bob    |Sales|1500  |python,spark|
|3  |Charlie|HR   |1200  |sql         |
|4  |David  |HR   |2000  |python,aws  |
+---+-------+-----+------+------------+

>>> rdd_map = rdd_emp.map(lambda x: (x[2], x[1].upper(), int(x[3] * 1.10)))
>>> print(rdd_map.collect())
[('Sales', 'ALICE', 1100), ('Sales', 'BOB', 1650), ('HR', 'CHARLIE', 1320), ('HR', 'DAVID', 2200)]
>>> df_map = df_emp.select(
...     "dept",
...     F.upper("name").alias("NAME_UPPER"),
...     (F.col("salary") * 1.10).cast("int").alias("salary_10pct")
... )
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
NameError: name 'F' is not defined
>>> df_map.show()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'df_map' is not defined. Did you mean: 'df_emp'?
>>> import pyspark.sql.functions as F
>>> df_map = df_emp.select(
...     "dept",
...     F.upper("name").alias("NAME_UPPER"),
...     (F.col("salary") * 1.10).cast("int").alias("salary_10pct")
... )
>>> df_map.show()
+-----+----------+------------+
| dept|NAME_UPPER|salary_10pct|
+-----+----------+------------+
|Sales|     ALICE|        1100|
|Sales|       BOB|        1650|
|   HR|   CHARLIE|        1320|
|   HR|     DAVID|        2200|
+-----+----------+------------+

>>> # Convert each employee row -> many (skill, 1) pairs
>>> rdd_flat = rdd_emp.flatMap(lambda x: [(skill, 1) for skill in x[4].split(",")])
>>> print(rdd_flat.collect())
[('sql', 1), ('spark', 1), ('python', 1), ('spark', 1), ('sql', 1), ('python', 1), ('aws', 1)]
>>> df_explode = (
...     df_emp
...     .withColumn("skill", F.explode(F.split(F.col("skills"), ",")))
...     .select("id", "name", "dept", "skill")
... )
>>> df_explode.show()
+---+-------+-----+------+
| id|   name| dept| skill|
+---+-------+-----+------+
|  1|  Alice|Sales|   sql|
|  1|  Alice|Sales| spark|
|  2|    Bob|Sales|python|
|  2|    Bob|Sales| spark|
|  3|Charlie|   HR|   sql|
|  4|  David|   HR|python|
|  4|  David|   HR|   aws|
+---+-------+-----+------+

>>> # (dept, salary) then reduce
>>> rdd_kv = rdd_emp.map(lambda x: (x[2], x[3]))
>>> rdd_reduce = rdd_kv.reduceByKey(lambda a, b: a + b)
>>> print(rdd_reduce.collect())
[('HR', 3200), ('Sales', 2500)]
>>> df_agg = df_emp.groupBy("dept").agg(F.sum("salary").alias("total_salary"))
>>> df_agg.show()
+-----+------------+
| dept|total_salary|
+-----+------------+
|Sales|        2500|
|   HR|        3200|
+-----+------------+

>>> # Make dept as key and keep the rest as value
>>> rdd_kv2 = rdd_emp.map(lambda x: (x[2], (x[1], x[3])))
>>> rdd_sorted = rdd_kv2.sortByKey(ascending=True)
>>> print(rdd_sorted.collect())
[('HR', ('Charlie', 1200)), ('HR', ('David', 2000)), ('Sales', ('Alice', 1000)), ('Sales', ('Bob', 1500))]
>>> df_sorted = df_emp.orderBy(F.col("dept").asc(), F.col("salary").asc())
>>> df_sorted.show()
+---+-------+-----+------+------------+
| id|   name| dept|salary|      skills|
+---+-------+-----+------+------------+
|  3|Charlie|   HR|  1200|         sql|
|  4|  David|   HR|  2000|  python,aws|
|  1|  Alice|Sales|  1000|   sql,spark|
|  2|    Bob|Sales|  1500|python,spark|
+---+-------+-----+------+------------+