kinesis-stream:
  Type: AWS::Kinesis::Stream
  Persist: true

  Configuration:
    Stream:
      Pipeline::Security:
        - Source:
            - lambda-analytics
            - ec2-cluster-shellscripts
          Allow: [ read, write ]
        - Source:
            - kinesis-deliverystream
          Allow: [ read]  
      Properties:
        RetentionPeriodHours: {{ vars.retentionperiod }}
        ShardCount: 5    