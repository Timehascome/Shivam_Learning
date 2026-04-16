>In Kinesis Data Streams, "partitions" are referred to as "shards." Shards are the base throughput unit of a Kinesis data stream.

>Definition: A shard is a uniquely identified sequence of data records in a stream. It's a logical partition that handles a subset of the stream's data.
 
>Partition Key: When data producers send records to a Kinesis stream, they must specify a "partition key." Kinesis uses this partition key to determine which shard a particular data record belongs to.

>Purpose: Ensures that all data records with the same partition key are routed to the same shard. This is crucial for maintaining the order of related records and for stateful processing.

>Distribution: A good partition key choice distributes data evenly across all shards to prevent hot shards (shards receiving disproportionately more data than others), which can lead to throttling.
 
>Sequence Number: Each data record within a shard has a sequence number, which is unique and strictly increasing. Consumers use this to track their position within a shard.

>Lifecycle: Shards have a lifecycle; they can be open, closed (after a split or merge operation), or expired. When a shard is split or merged, it creates new child shards, and the parent shards eventually close.

>Consumer Groups: Each consumer group can read independently from the shards. For example, two different Kinesis applications (consumer groups) can process the same data in the same stream concurrently without interfering with each other's progress.