>>How to configure logs ?
>Under the Load balancer attriubtes section can edit access log and add s3 path URI where we want the logs to be stored.
>The S3 bucket must have a bucket policy that grants the Elastic Load Balancing (ELB) service permission to write logs to it. Should be in same region

>>What about cloudwatch logs? (Optional)
> Direct integration is not available to cloudwatch
> Configure Lambda to be invoked by S3 (e.g., s3:ObjectCreated:*) when new logs are added