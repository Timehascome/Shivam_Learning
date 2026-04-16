lambda-analytics:
  Type: AWS::Serverless

  DependsOn:
    - alb-analytics
    - kinesis-analytics

  Inputs:
    listenerArnInput:
      Value:
        Fn::Pipeline::GetOutput:
          Component: alb-analytics
          OutputName: ListenerArn
    StreamNameInput:
      Value:
        Fn::Pipeline::GetOutput:
          Component: kinesis-analytics
          OutputName: StreamName            

  Configuration:
    Function:
      Properties:
        Code:
          S3Key:
            Fn::Pipeline::FileS3Key:
              Path: lambda-analytics.zip
        Handler: index.handler
        MemorySize: {{ vars.lambdaMemorySize }}
        Runtime: python3.12
        Timeout: {{ vars.lambdaTimeout }}
        Environment:
          Variables:
            csAWSUrl: {{ vars.csAWSUrl }}
            csMarketPlaceUrl: {{ vars.csMarketPlaceUrl }}
            StreamName: 
              Ref: StreamNameInput       


    ListenerRule:
      Properties:
        Conditions:
        - Field: path-pattern
          Values:
          - "/analyticsws/rest/eventLogger/analytics"
        ListenerArn: !Ref listenerArnInput
        Priority: 1          

    
    LogGroup:
      Properties:
        RetentionInDays: 7