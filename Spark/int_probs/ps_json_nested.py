#get me a json file with nested objects and arrays, and write a pyspark  script to parse it and print the values of the nested objects and arrays.
#Here is an example of a JSON file with nested objects and arrays:
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode       
# Create a SparkSession
spark = SparkSession.builder.appName("ParseNestedJSON").getOrCreate()   
# Read the JSON file into a DataFrame
df = spark.read.json("path/to/your/jsonfile.json")  
#why not use multiline as true in spark.read.json? Because the JSON file is not in a multiline format, it is a single JSON object. If the JSON file were in a multiline format (i.e., each line is a separate JSON object), then we would use the option multiline=True to read it correctly. In this case, since the JSON file is a single object, we can read it without the multiline option.
# Select the nested objects and arrays
df.select("name", "age", "address.street", "address.city", "address.state", "address.zip", explode("phoneNumbers").alias("phone")) \
    .select("name", "age", "street", "city", "state", "zip", "phone.type", "phone.number") \
    .show(truncate=False)   # Stop the SparkSession
spark.stop()        