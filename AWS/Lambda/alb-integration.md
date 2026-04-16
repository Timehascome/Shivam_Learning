1) When deploying lambda service how do you integrate the ALB as listerner input with route logics?
 # We can use the already deployed ALB inside Lambda yml deploy file 
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

2) why you would choose ALB with Lambda over other options (like API Gateway) for specific scenarios?
> 	                       API GW	        ALB
Request/seconds	 ==  Limited to 10000	virtually unlimited
Routing          ==  Path based         Path base and others like Requesters IP, Http Headers, Http method, etc
Cost             ==  Pay per request    Pay by time + Request (Load Balancer Capacity Units)
Serverless Scalability: Leverages Lambda's automatic scaling for web and API-based workloads, ensuring high availability and optimized performance. 
Simplified Architecture: Reduces the need for EC2 instances or containers, simplifying operational complexity and costs

