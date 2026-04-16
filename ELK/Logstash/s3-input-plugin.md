>>S3 input plugin allows logstash to consume data fromm aws s3 buckets. Configure it to monitor s3 buckets , paths, and even use SQS for event notifications to trigger new file processing. It plays an important role in batch processing as s3 usually contains large files to be read in chunks. Key Configurations:

input {
    s3{
        bucket => "internet-analytics"
        region => "ap-southeast-1"
        role_arn => "arn:aws:iam::1234:role/role-user-auto-sg-g1-dbsa-s3read"
        role_session_name => "role-user-auto-sg-g1-abcd-s3read"
        codec => "json"
        type => "s3"
        prefix => "FIREHOSECLICKSTREAM/"
        interval => "300"
    }
}