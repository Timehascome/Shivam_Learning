Pipelines are the core of logstash functionality , defining the flow of data from input to output. The Logstash pipeline consists of three main stages : input, filter, and output. Multiple inputs can be fed into a pipeline , filters can transform and enrich data and output send processed data to various destinations. Sequential execution of processors within a pipeline and conditional logic can be applied to route events.

input {}

filter {}

output {}