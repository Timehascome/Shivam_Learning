>>> from pyspark.sql.functions import col
>>> data_l =[(1,"ALice","Sales"),(2,"Bob","HR"),(3,"Charlie","Engineering"),(4,"David","Marketing"),(6,"Frank","Sales")]
>>> columns_l = ["id","name","department"]
>>> df_l = spark.createDataFrame(data_l, columns_l)
>>> df_l.show(5)
+---+-------+-----------+
| id|   name| department|
+---+-------+-----------+
|  1|  ALice|      Sales|
|  2|    Bob|         HR|
|  3|Charlie|Engineering|
|  4|  David|  Marketing|
|  6|  Frank|      Sales|
+---+-------+-----------+

>>> data_r = [(1,"NewYork"),(3,"London"),(5,"Paris"),(1,"SF")]
>>> columns_r=["id","city"]
>>> df_r = spark.createDataFrame(data_r, columns_r)
>>> df_r.show()
+---+-------+
| id|   city|
+---+-------+
|  1|NewYork|
|  3| London|
|  5|  Paris|
|  1|     SF|
+---+-------+

>>> df_l.join(df_r, on="id",how="inner").show()
+---+-------+-----------+-------+
| id|   name| department|   city|
+---+-------+-----------+-------+
|  1|  ALice|      Sales|NewYork|
|  1|  ALice|      Sales|     SF|
|  3|Charlie|Engineering| London|
+---+-------+-----------+-------+

>>> df_l.join(df_r, on="id",how="left").show()
+---+-------+-----------+-------+
| id|   name| department|   city|
+---+-------+-----------+-------+
|  1|  ALice|      Sales|     SF|
|  1|  ALice|      Sales|NewYork|
|  2|    Bob|         HR|   NULL|
|  3|Charlie|Engineering| London|
|  4|  David|  Marketing|   NULL|
|  6|  Frank|      Sales|   NULL|
+---+-------+-----------+-------+

>>> df_l.join(df_r, on="id",how="right").show()
+---+-------+-----------+-------+
| id|   name| department|   city|
+---+-------+-----------+-------+
|  1|  ALice|      Sales|NewYork|
|  3|Charlie|Engineering| London|
|  5|   NULL|       NULL|  Paris|
|  1|  ALice|      Sales|     SF|
+---+-------+-----------+-------+

>>> df_l.join(df_r, on="id",how="left_semi").show()
+---+-------+-----------+
| id|   name| department|
+---+-------+-----------+
|  1|  ALice|      Sales|
|  3|Charlie|Engineering|
+---+-------+-----------+

>>> df_l.join(df_r, on="id",how="left_anti").show()
+---+-----+----------+
| id| name|department|
+---+-----+----------+
|  2|  Bob|        HR|
|  4|David| Marketing|
|  6|Frank|     Sales|
+---+-----+----------+

>>> df_l.join(df_r, on="id",how="cross").show()
+---+-------+-----------+-------+
| id|   name| department|   city|
+---+-------+-----------+-------+
|  1|  ALice|      Sales|NewYork|
|  1|  ALice|      Sales|     SF|
|  3|Charlie|Engineering| London|
+---+-------+-----------+-------+

BROADCAST: one side small enough, fastest, avoid shuffle

SHUFFLE_HASH: one side smaller-ish, avoid sorts, can be faster than SMJ

MERGE (SMJ): both large, stable default, but pays sort cost

>>> spark.conf.get("spark.sql.autoBroadcastJoinThreshold")
'10485760b'

>>> from pyspark.sql.functions import to_date, to_timestamp
>>> data_events=[("event1","2026-01-08 10:05:00"),("event2","2026-01-08 11:30:00"),("event3","2026-01-09 09:15:00")]
>>> data_windows=[('windowA','2026-01-08 10:00:00"','2026-01-08 11:00:00"'),('windowB','2026-01-08 10:00:00"','2026-01-08 11:00:00"'),('windowC','2026-01-08 10:00:00"','2026-01-08 11:00:00"'),('windowD','2026-01-08 10:00:00"','2026-01-08 11:00:00"')]
>>> to_timestamp("2026-01-08 10:00:00")
Column<'to_timestamp(2026-01-08 10:00:00)'>
>>> to_timestamp("2026-01-08 10:00:00").show()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'Column' object is not callable
>>> time=to_timestamp("2026-01-08 10:00:00")
>>> time
Column<'to_timestamp(2026-01-08 10:00:00)'>
>>> ti_date=to_date("2026-01-08 10:00:00")
>>> ti_date
Column<'to_date(2026-01-08 10:00:00)'>
>>> df_events=spark.createDataFrame(data_events,['event_id','event_timestamp']).withColumn('event_timestamp',to_timestamp(col("event_timestamp"))).withColumn("event_date",to_date(col("event_timestamp")))
>>> df_events.show()
+--------+-------------------+----------+
|event_id|    event_timestamp|event_date|
+--------+-------------------+----------+
|  event1|2026-01-08 10:05:00|2026-01-08|
|  event2|2026-01-08 11:30:00|2026-01-08|
|  event3|2026-01-09 09:15:00|2026-01-09|
+--------+-------------------+----------+

>>> df_time_windows=spark.createDataFrame(data_windows,["window_id","start_time","end_time"]).withColumn("start_time,to_timestamp(col("start_time"))).withColumn("end_time,to_timestamp(col("end_time"))).withColumn("window_start_date,to_date(col("start_time"))).withColumn("window_end_date,to_date(col("start_time")))
  File "<stdin>", line 1
    df_time_windows=spark.createDataFrame(data_windows,["window_id","start_time","end_time"]).withColumn("start_time,to_timestamp(col("start_time"))).withColumn("end_time,to_timestamp(col("end_time"))).withColumn("window_start_date,to_date(col("start_time"))).withColumn("window_end_date,to_date(col("start_time")))
                                                                                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
>>> df_time_windows=spark.createDataFrame(data_windows,["window_id","start_time","end_time"]).withColumn("start_time,to_timestamp(col("start_time"))).withColumn("end_time,to_timestamp(col("end_time"))).withColumn("window_start_date,to_date(col("start_time"))).withColumn("window_end_date",to_date(col("start_time")))
  File "<stdin>", line 1
    df_time_windows=spark.createDataFrame(data_windows,["window_id","start_time","end_time"]).withColumn("start_time,to_timestamp(col("start_time"))).withColumn("end_time,to_timestamp(col("end_time"))).withColumn("window_start_date,to_date(col("start_time"))).withColumn("window_end_date",to_date(col("start_time")))
                                                                                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
>>> df_time_windows=spark.createDataFrame(data_windows,["window_id","start_time","end_time"]).withColumn("start_time",to_timestamp(col("start_time"))).withColumn("end_time",to_timestamp(col("end_time"))).withColumn("window_start_date",to_date(col("start_time"))).withColumn("window_end_date",to_date(col("start_time")))
>>> df_time_windows.show()
+---------+----------+--------+-----------------+---------------+
|window_id|start_time|end_time|window_start_date|window_end_date|
+---------+----------+--------+-----------------+---------------+
|  windowA|      NULL|    NULL|             NULL|           NULL|
|  windowB|      NULL|    NULL|             NULL|           NULL|
|  windowC|      NULL|    NULL|             NULL|           NULL|
|  windowD|      NULL|    NULL|             NULL|           NULL|
+---------+----------+--------+-----------------+---------------+

>>> data_windows
[('windowA', '2026-01-08 10:00:00"', '2026-01-08 11:00:00"'), ('windowB', '2026-01-08 10:00:00"', '2026-01-08 11:00:00"'), ('windowC', '2026-01-08 10:00:00"', '2026-01-08 11:00:00"'), ('windowD', '2026-01-08 10:00:00"', '2026-01-08 11:00:00"')]
>>> df_time_windows=spark.createDataFrame(data_windows,["window_id","start_time","end_time"]).withColumn("start_time",to_timestamp(col("start_time"))).withColumn("end_time",to_timestamp(col("end_time"))).withColumn("window_start_date",to_date(col("start_time"))).withColumn("window_end_date",to_date(col("end_time")))
>>> df_time_windows.show()
+---------+----------+--------+-----------------+---------------+
|window_id|start_time|end_time|window_start_date|window_end_date|
+---------+----------+--------+-----------------+---------------+
|  windowA|      NULL|    NULL|             NULL|           NULL|
|  windowB|      NULL|    NULL|             NULL|           NULL|
|  windowC|      NULL|    NULL|             NULL|           NULL|
|  windowD|      NULL|    NULL|             NULL|           NULL|
+---------+----------+--------+-----------------+---------------+

>>> data_windows=[('windowA','2026-01-08 10:00:00','2026-01-08 11:00:00'),('windowB','2026-01-08 10:00:00','2026-01-08 11:00:00'),('windowC','2026-01-08 10:00:00','2026-01-08 11:00:00'),('windowD','2026-01-08 10:00:00','2026-01-08 11:00:00')]
>>> df_time_windows=spark.createDataFrame(data_windows,["window_id","start_time","end_time"]).withColumn("start_time",to_timestamp(col("start_time"))).withColumn("end_time",to_timestamp(col("end_time"))).withColumn("window_start_date",to_date(col("start_time"))).withColumn("window_end_date",to_date(col("end_time")))
>>> df_time_windows.show()
+---------+-------------------+-------------------+-----------------+---------------+
|window_id|         start_time|           end_time|window_start_date|window_end_date|
+---------+-------------------+-------------------+-----------------+---------------+
|  windowA|2026-01-08 10:00:00|2026-01-08 11:00:00|       2026-01-08|     2026-01-08|
|  windowB|2026-01-08 10:00:00|2026-01-08 11:00:00|       2026-01-08|     2026-01-08|
|  windowC|2026-01-08 10:00:00|2026-01-08 11:00:00|       2026-01-08|     2026-01-08|
|  windowD|2026-01-08 10:00:00|2026-01-08 11:00:00|       2026-01-08|     2026-01-08|
+---------+-------------------+-------------------+-----------------+---------------+

>>> df_events.show()
+--------+-------------------+----------+
|event_id|    event_timestamp|event_date|
+--------+-------------------+----------+
|  event1|2026-01-08 10:05:00|2026-01-08|
|  event2|2026-01-08 11:30:00|2026-01-08|
|  event3|2026-01-09 09:15:00|2026-01-09|
+--------+-------------------+----------+