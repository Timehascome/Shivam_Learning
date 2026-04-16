Business Goal : Get performance metrics of api's for each country based on the elapsed time passed from source.
Data Flow : Data flows from ALB > Lambda > Kinesis > Firehose > S3 > Logstash > Elastic Index (source for this code)
            Writes back to elastic index
Execution tye : Batch (scheduled) and frequency : daily job.

Code : 
 >> elastic connection is not established just a mock return has been used for execution
 >> single channel is used multiple channels can be configured with multiple queries

 Questions :
 >> How do you establish authentication with elastic ?  
      >create a separate module authentication.py and follow company standards
 >> How do we judge if the aggregated data returned by query and the query execution will not be a performance bottle neck ? 
      >Query and  code should be tested in the UAT based on resource capacity
 >> What python components are mostly used ?
     > pandas for data manipulation and cleaning and transformations.
     > Elastic query to read data in aggregated manner / just like regular SQL in structured data cases.


 Summary : This project gives a high level view how data can be fetched and transformed from ELK nosql db and transformed and written back to elastic index for further reporting.    

