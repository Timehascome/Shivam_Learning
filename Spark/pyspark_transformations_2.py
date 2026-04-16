df_iris.show(5)
+------------+-----------+------------+-----------+-------+
|sepal.length|sepal.width|petal.length|petal.width|variety|
+------------+-----------+------------+-----------+-------+
|         5.1|        3.5|         1.4|        0.2| Setosa|
|         4.9|        3.0|         1.4|        0.2| Setosa|
|         4.7|        3.2|         1.3|        0.2| Setosa|
|         4.6|        3.1|         1.5|        0.2| Setosa|
|         5.0|        3.6|         1.4|        0.2| Setosa|
+------------+-----------+------------+-----------+-------+
 df_iris_rename_col= df_iris.toDF("sepal_length", "sepal_width", "petal_length", "petal_width", "variety")
 df_iris_rename_col.show(5)
+------------+-----------+------------+-----------+-------+
|sepal_length|sepal_width|petal_length|petal_width|variety|
+------------+-----------+------------+-----------+-------+
|         5.1|        3.5|         1.4|        0.2| Setosa|
|         4.9|        3.0|         1.4|        0.2| Setosa|
|         4.7|        3.2|         1.3|        0.2| Setosa|
|         4.6|        3.1|         1.5|        0.2| Setosa|
|         5.0|        3.6|         1.4|        0.2| Setosa|
+------------+-----------+------------+-----------+-------+
df_iris_sepal_area=df_iris_rename_col.withColumn("sepal_area",col("sepal_length")*col("sepal_width"))
df_iris_sepal_area.show(5)
+------------+-----------+------------+-----------+-------+------------------+
|sepal_length|sepal_width|petal_length|petal_width|variety|        sepal_area|
+------------+-----------+------------+-----------+-------+------------------+
|         5.1|        3.5|         1.4|        0.2| Setosa|17.849999999999998|
|         4.9|        3.0|         1.4|        0.2| Setosa|14.700000000000001|
|         4.7|        3.2|         1.3|        0.2| Setosa|15.040000000000001|
|         4.6|        3.1|         1.5|        0.2| Setosa|             14.26|
|         5.0|        3.6|         1.4|        0.2| Setosa|              18.0|
+------------+-----------+------------+-----------+-------+------------------+
df_iris_sepal_area=df_iris_sepal_area.withColumn("sepal_area", round(col("sepal_area"),2))
df_iris_sepal_area.show(5)
+------------+-----------+------------+-----------+-------+----------+
|sepal_length|sepal_width|petal_length|petal_width|variety|sepal_area|
+------------+-----------+------------+-----------+-------+----------+
|         5.1|        3.5|         1.4|        0.2| Setosa|     17.85|
|         4.9|        3.0|         1.4|        0.2| Setosa|      14.7|
|         4.7|        3.2|         1.3|        0.2| Setosa|     15.04|
|         4.6|        3.1|         1.5|        0.2| Setosa|     14.26|
|         5.0|        3.6|         1.4|        0.2| Setosa|      18.0|

df_iris_sepal_area_null = df_iris_sepal_area.withColumn("sepal_area",when(col("sepal_area")<15,None).otherwise(col("sepal_area")))
df_iris_sepal_area_null.show(5)
+------------+-----------+------------+-----------+-------+----------+
|sepal_length|sepal_width|petal_length|petal_width|variety|sepal_area|
+------------+-----------+------------+-----------+-------+----------+
|         5.1|        3.5|         1.4|        0.2| Setosa|     17.85|
|         4.9|        3.0|         1.4|        0.2| Setosa|      NULL|
|         4.7|        3.2|         1.3|        0.2| Setosa|     15.04|
|         4.6|        3.1|         1.5|        0.2| Setosa|      NULL|
|         5.0|        3.6|         1.4|        0.2| Setosa|      18.0|
+------------+-----------+------------+-----------+-------+----------+

df_na=df_iris_sepal_area_null.na.fill(0)
df_na.show(5)
+------------+-----------+------------+-----------+-------+----------+
|sepal_length|sepal_width|petal_length|petal_width|variety|sepal_area|
+------------+-----------+------------+-----------+-------+----------+
|         5.1|        3.5|         1.4|        0.2| Setosa|     17.85|
|         4.9|        3.0|         1.4|        0.2| Setosa|       0.0|
|         4.7|        3.2|         1.3|        0.2| Setosa|     15.04|
|         4.6|        3.1|         1.5|        0.2| Setosa|       0.0|
|         5.0|        3.6|         1.4|        0.2| Setosa|      18.0|
+------------+-----------+------------+-----------+-------+----------+

df_na_zero_area =df_na.filter(col("sepal_area")==0)
df_na_zero_area.show(5)
+------------+-----------+------------+-----------+-------+----------+
|sepal_length|sepal_width|petal_length|petal_width|variety|sepal_area|
+------------+-----------+------------+-----------+-------+----------+
|         4.9|        3.0|         1.4|        0.2| Setosa|       0.0|
|         4.6|        3.1|         1.5|        0.2| Setosa|       0.0|
|         4.4|        2.9|         1.4|        0.2| Setosa|       0.0|
|         4.8|        3.0|         1.4|        0.1| Setosa|       0.0|
|         4.3|        3.0|         1.1|        0.1| Setosa|       0.0|
+------------+-----------+------------+-----------+-------+----------+


