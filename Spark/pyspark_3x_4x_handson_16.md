Spark 3.x:
> Introduced AQE which could identify skewed joins and change startegy of join or partitiones coalesced
> .config(spark.sql.adaptive.enabled , true)
> .config(spark.sql.adaptive.coalescedPartitions.enabled , true)
> .config(spark.sql.adaptive.skewJoin.enabled , true)
> .config(spark.sql.adaptive.localShuffleReader.enabled , true) #“Local shuffle reader means the reducer task reads shuffle blocks directly from the same executor’s local memory or disk, bypassing network transfer. This is possible only with AQE because Spark needs runtime statistics to co-locate tasks and data.”

>Introduced dynamic-partitioning-pruning:
>spark.sql.sources.partitionOverwriteMode, "dynamic"
>spark.sql.optimizer.dyna,icPartitionPruning.enable, "true"
>.enableHiveSupport()  needs hive support for this feature

>Introduced Pandas API on spark
import pyspark.pandas as ps
import pandas as pd

pandas_df = pd.DataFrame({'id':[],'name':[],'score':[]}) #python pandas
spark_pandas_df =ps.from_pandas(pandas_df)  #converted to spark pandas
spark_df_from_koalas = saprk_pandas_df.to_spark() #converts to pure spark df
The moment you convert to real pandas (to_pandas()), you’re back on the driver RAM.


Spark 4.x:
> Introduced ANSI SQL Mode by Default, spark.sql.ansi.enabled
>VARIANT data type : efficinet handling of semistructured data especially json.
> |> pipe operator :
SELECT name
FROM users
|> SELECT trim(name) AS name
|> SELECT upper(name) AS name

> string collation support

#what is from_json >> Convert JSON string → Struct / Map, to_json, get_json_object?

