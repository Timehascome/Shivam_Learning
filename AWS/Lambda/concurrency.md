>>In AWS Lambda, concurrency refers to the number of simultaneous executions of your function. When your Lambda function is invoked, AWS Lambda provisions an execution environment to run your code. If multiple requests arrive concurrently, Lambda scales by creating more execution environments to handle each request in parallel, up to a certain limit

>>How are we handling?
 > Ondemand Concurrency (Default)
 > 24000 unprovisioned concurrenct is set for Account current which all Lambdas share
 > We hit 1000-7000 concurrent executions at Min and Max Level across 3 lambda functions (4500 + 1000 + 1500)
 > Use DLQ of SNS if request goes unprocessed , can set maximum age of event eg : 6h
 > average duration of processing is 100 ms per lambda so total concurrent executions for 5000 requests per second will be 5000*0.1 ~ 500

 Pros:
 > Automatic scaling based on unreserved limit.
 > We have unpredictable traffic patterns where occasional cold starts are acceptable
 > Provisioned and Reserved concurrency are not needed as these need predictable traffic.
 > Cost is per invoke and duration of compute.

 Cons:
 > Uncontrolled traffic can lead to excessive resource consumption, throttling errors, and increased costs during traffic spikes. > Can also overload downstream applications.
 > Cold starts might delay instance up time from low to high peak hours.
 > If one function has sudden surge and consumes large portion of unreserved , request might get throttled  (429 error)


 Some important points:
 > Reserved Concurrency vs  Provisioned Concurrency == guaranteeing resources vs. eliminating cold starts
 > CloudWatch metrics like ConcurrentExecutions and Throttles provide insights into real-time usage and potential issues

