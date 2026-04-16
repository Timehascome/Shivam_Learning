 >>An Application Load Balancer (ALB) works by receiving incoming application traffic, such as HTTP or HTTPS requests, and intelligently routing it to different targets (like servers or containers) based on rules you define.

>My current traffic ? HTTPS
>My Target ? Lambda 
>How have you defined the rule for target ? The listener input and rule can be defined when deploying the target Lambda service.
>What other targets can you configure ? Ec2, IP instances etc..

>>It operates at the application layer (Layer 7), allowing it to make routing decisions based on the content of the request, such as the URL path or hostname. Key components include a listener that accepts requests, rules that define routing logic, and target groups that organize the registered targets. 

> Can you write a simple yaml which can deploy ALB with above features ?
# Application Load Balancer component for Lambda
alb-analytics:
  Type: AWS::ApplicationLoadBalancer
  Persist: false

  Configuration:
     
  Listener:
     Properties:
       Certificates:
        - CertificateArn : {{vars.arnName}}
        Port : '443'
        Protocal: HTTPS

 # We can use the above ALB inside Lambda yml deploy file 
 lambda-analytics:
  Type: AWS::Serverless

  DependsOn:
    - alb-analytics

  Inputs:
    listenerArnInput:
      Value:
        Fn::Pipeline::GetOutput:
          Component: alb-analytics
          OutputName: ListenerArn   


 ListenerRule:
    Properties:
       Conditions:
        - Field: path-pattern
          Values:
          - "/analytics/rest/eventLogger/"
        ListenerArn: !Ref listenerArnInput
        Priority: 4            


