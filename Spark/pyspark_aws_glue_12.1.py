#write a code to read data from s3 using aws glue pyspark
import sys      
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions    
from pyspark.context import SparkContext    
from awsglue.context import GlueContext 
from awsglue.job import Job 
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
import boto3
import pandas as pd

args = getResolvedOptions(sys.argv, ['JOB_NAME','s3_input_path','s3_output_path'])  
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session       
job = Job(glueContext)
job.init(args['JOB_NAME'], args)        
s3_input_path = args['s3_input_path']
s3_output_path = args['s3_output_path'] 
# Read data from S3
input_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [s3_input_path]},
    format="parquet"
)       
# Convert DynamicFrame to DataFrame
input_df = input_dynamic_frame.toDF()   
# Perform transformations (example: filter rows where a column 'value' > 100)
transformed_df = input_df.filter(col('value') > 100)
# Convert DataFrame back to DynamicFrame    
output_dynamic_frame = DynamicFrame.fromDF(transformed_df, glueContext, "output_dynamic_frame")
# Write data back to S3 
glueContext.write_dynamic_frame.from_options(
    frame=output_dynamic_frame,
    connection_type="s3",
    connection_options={"path": s3_output_path},
    format="parquet"
)       
job.commit()   




