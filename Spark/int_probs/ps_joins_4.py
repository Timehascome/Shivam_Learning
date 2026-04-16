#joins in pyspark left_semi, left_anti, right_semi, right_anti, inner, outer, left_outer, right_outer
#left_semi - returns all the records from the left dataframe that have a match in the
#right_semi - returns all the records from the right dataframe that have a match in the left dataframe
#left_anti - returns all the records from the left dataframe that do not have a match
#right_anti - returns all the records from the right dataframe that do not have a match in the left dataframe
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\orders.csv 
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\order_products__prior.csv
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\order_products__train.csv
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\aisles.csv 
#path = C:\Users\399sh\Desktop\git\Shivam_Learning\Spark\int_probs\archive\products.csv

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Joins").getOrCreate()
orders = spark.read.csv("C:/Users/399sh/Desktop/git/Shivam_Learning/Spark/int_probs/archive/orders.csv", header=True, inferSchema=True)
order_products_prior = spark.read.csv("C:/Users/399sh/Desktop/git/Shivam_Learning/Spark/int_probs/archive/order_products__prior.csv", header=True, inferSchema=True)
order_products_train = spark.read.csv("C:/Users/399sh/Desktop/git/Shivam_Learning/Spark/int_probs/archive/order_products__train.csv", header=True, inferSchema=True)
aisles = spark.read.csv("C:/Users/399sh/Desktop/git/Shivam_Learning/Spark/int_probs/archive/aisles.csv", header=True, inferSchema=True)
products = spark.read.csv("C:/Users/399sh/Desktop/git/Shivam_Learning/Spark/int_probs/archive/products.csv", header=True, inferSchema=True) 
#inner join
inner_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "inner")
inner_join_df.show(5)   
#left_outer join
left_outer_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "left_outer")
left_outer_join_df.show(5)
#right_outer join
right_outer_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "right_outer")
right_outer_join_df.show(5)
#full_outer join    
full_outer_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "full_outer")
full_outer_join_df.show(5)  
#left_semi join
left_semi_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "left_semi")
left_semi_join_df.show(5)
#right_semi join    
right_semi_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "right_semi")
right_semi_join_df.show(5)  
#left_anti join
left_anti_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "left_anti")
left_anti_join_df.show(5)   
#right_anti join
right_anti_join_df = orders.join(order_products_prior, orders.order_id == order_products_prior.order_id, "right_anti")
right_anti_join_df.show(5)

#multi column join
multi_column_join_df = orders.join(order_products_prior, (orders.order_id == order_products_prior.order_id) & (orders.user_id == order_products_prior.user_id), "inner")
multi_column_join_df.show(5)    

#one more way to do multi column join
multi_column_join_df_2 = orders.join(order_products_prior, ["order_id", "user_id"], "inner")
multi_column_join_df_2.show(5)      

#one more way to specify type of join
multi_column_join_df_3 = orders.join(order_products_prior, ["order_id", "user_id"], how="inner")
multi_column_join_df_3.show(5)  

#multi column join with alias and on condition
orders_alias = orders.alias("o")
order_products_prior_alias = order_products_prior.alias("opp")
multi_column_join_df_4 = orders_alias.join(order_products_prior_alias, (orders_alias.order_id == order_products_prior_alias.order_id) & (orders_alias.user_id == order_products_prior_alias.user_id), "inner")
multi_column_join_df_4.show(5)

#with on condition
multi_column_join_df_5 = orders.join(order_products_prior, on=(orders.order_id == order_products_prior.order_id) & (orders.user_id == order_products_prior.user_id), how="inner")
multi_column_join_df_5.show(5)


#broadcast join
from pyspark.sql.functions import broadcast 
broadcast_join_df = orders.join(broadcast(order_products_prior), orders.order_id == order_products_prior.order_id, "inner")
broadcast_join_df.show(5)       

#shuffle hash join
shuffle_hash_join_df = orders.join(order_products_prior.hint("shuffle_hash"), orders.order_id == order_products_prior.order_id, "inner")
shuffle_hash_join_df.show(5)

#sort merge join
sort_merge_join_df = orders.join(order_products_prior.hint("sort_merge"), orders.order_id == order_products_prior.order_id, "inner")
sort_merge_join_df.show(5)      