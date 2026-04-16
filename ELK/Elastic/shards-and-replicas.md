>Shards and replicas are backbone for elastic search's scalability, performance and high availability.
>Key concepts :
 >> Shard is a horizontal partition of an index that holds a subset of the documents.
 >>They enable horizontal scaling and parallel perocessing of queries acroos nodes.
 >>too many small shards can lead to overhead while too few shards hinder performance and recovery.
 >>1 to 4 primary shards per node and max 20 shards per index.
 >> Replicasc are exact copies 
    >>> Primary and replica shards are placed in different nodes for fault tolerance
    >>> Ensures data avilability even if node fails.
    >>> Can use index templates to define default setting for new indices , including number of shards and indices.
    >>> _cat/shards