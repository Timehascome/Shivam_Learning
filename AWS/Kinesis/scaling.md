>Scaling in Kinesis Data Streams is managed through shards.
>Shard-based Scaling: A Kinesis Data Stream's capacity is determined by the number of shards it contains. Each shard provides a  fixed unit of capacity:
      >Write Capacity: 1 MB/second or 1,000 records/second.
      >Read Capacity: 2 MB/second or 5 transactions/second (for standard consumers).
      >Manual Resharding: You can manually increase (split) or decrease (merge) the number of shards in a stream to adjust its capacity.
      >Split: Divides an existing shard into two new shards, increasing write and read capacity. This is useful for handling increasing data ingestion rates or processing load.
      >Merge: Combines two adjacent shards into one, decreasing capacity and potentially saving costs if traffic reduces.
      >On-Demand Capacity Mode: Kinesis Data Streams offers an on-demand capacity mode where you don't specify shard counts. Kinesis automatically manages the shards for you, scaling capacity up or down based on your throughput. This is suitable for unpredictable workloads and simplifies management, but can be more expensive for consistent, high-throughput workloads compared to provisioned mode.
      >Monitoring: Use Amazon CloudWatch metrics (e.g., IncomingBytes, IncomingRecords, ReadProvisionedThroughputExceeded, WriteProvisionedThroughputExceeded) to monitor stream utilization and determine when to scale.