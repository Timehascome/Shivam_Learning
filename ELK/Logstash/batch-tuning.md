>> Batch tuning is critical for optimizing Logstash pipelines, especially with high data volumes.
>> Configure parameters in logstash.yml such as:
   > pipeline.batch.size : 125 #default , can make 1000
   > pipeline.batch.delay : 5 #default  , can make 1000 for sec delay
   > pipeline.workers: 1 # Often defaults based on CPU cores, but manual tuning is common.
   > pipeline.ecs_compatibility : disabled # v8 depending on version
   # Enable persistent queue for data durability
   path.queue : "/var/lib/logstash/queue/"
   pipeline.individaul_dead_letter_queue: true # recommended granular DLQ per pipeline.