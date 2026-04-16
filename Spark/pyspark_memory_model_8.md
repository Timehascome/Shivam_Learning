# Spark Memory Model — Complete Revision Guide

This document provides a **clear, production-grade understanding of Spark’s memory model**, covering **Driver Memory**, **Executor Memory**, **Unified Memory**, **Off-Heap (Tungsten)**, **OOM scenarios**, and **best practices**.

---

## 1. Driver Memory

The **Driver** is the master process responsible for:
- DAG creation
- Task scheduling
- Metadata management
- Collecting results

### 1.1 Driver Memory Components

+--------------------------------------------------+
| Driver Total Memory |
+--------------------------------------------------+
| Driver JVM Heap (spark.driver.memory) |
| - DAG metadata |
| - Task results |
| - Broadcast variables |
+--------------------------------------------------+
| Driver Memory Overhead |
| (spark.driver.memoryOverhead) |
| - PySpark processes |
| - Network buffers |
| - Non-JVM native memory |
+--------------------------------------------------+


### 1.2 Default Values

- `spark.driver.memory` → **1 GB** (default)
- `spark.driver.memoryOverhead`  
max(384MB, 0.10 * spark.driver.memory)


### 1.3 Common Driver OOM Scenarios

| Cause | Explanation |
|-----|------------|
| Large `.collect()` | Pulls entire dataset to driver |
| Large `.toPandas()` | Converts Spark DF to Pandas in driver |
| Large broadcast vars | Broadcast data too big for driver heap |
| Complex DAGs | Huge metadata overhead |
| Too many partitions | Shuffle metadata overload |

**Rule:** Driver is **not** meant for large data processing.
## 2. Executor Memory

Executors perform **actual data processing**.

### 2.1 Executor Memory Layout
+--------------------------------------------------+
| Executor Total Memory |
+--------------------------------------------------+
| Reserved Memory (300MB fixed) |
+--------------------------------------------------+
| User Memory |
| - UDFs |
| - User-defined objects |
+--------------------------------------------------+
| Spark Memory (Unified Memory Region) |
| +--------------------------------------------+ |
| | Execution Memory (joins, shuffles, sorts) | |
| +--------------------------------------------+ |
| | Storage Memory (cache, persist) | |
| +--------------------------------------------+ |
+--------------------------------------------------+
| Memory Overhead |
| (Off-heap, PySpark, JVM overhead) |
+--------------------------------------------------+


---

## 3. Unified Memory Model

Spark dynamically shares memory between **execution** and **storage**.

### 3.1 Key Configuration

| Config | Default | Purpose |
|------|--------|--------|
| `spark.memory.fraction` | 0.6 | Portion of JVM heap for Spark |
| `spark.memory.storageFraction` | 0.5 | Storage portion of unified memory |

---

### 3.2 Unified Memory Calculation (Example)

Assume:
- `spark.executor.memory = 8GB (8192MB)`
- Reserved Memory = 300MB


⚠️ Storage can **borrow** from execution, but **execution cannot evict execution memory**.

---

## 4. Memory Overhead

Memory outside JVM heap.

### 4.1 What Uses Memory Overhead?

- PySpark worker processes
- Native libraries
- JVM metadata
- Thread stacks
- Network buffers

### 4.2 Default Calculation


---

## 5. Off-Heap Memory (Project Tungsten)

Off-heap memory is **outside JVM heap**, managed directly by Spark.

### 5.1 Why Off-Heap?

- Reduces GC pauses
- Faster binary processing
- Fewer Java objects
- Better cache locality

### 5.2 Tungsten Features

- Custom memory manager
- UnsafeRow binary format
- Whole-Stage Code Generation
- Efficient serialization

### 5.3 Configuration

```conf
spark.memory.offHeap.enabled = true
spark.memory.offHeap.size = 4g
6. Cache vs Persist
6.1 cache()


Shortcut for persist()


Default storage level:


RDD → MEMORY_ONLY


DataFrame → MEMORY_AND_DISK




6.2 persist() Storage Levels
LevelDescriptionMEMORY_ONLYFast, high memory usageMEMORY_AND_DISKSpills to diskMEMORY_ONLY_SERSerialized, memory efficientMEMORY_AND_DISK_SERSerialized + spillDISK_ONLYSlow, safeOFF_HEAPUses off-heap memory
Suffix _2 → Replication across 2 nodes.
⚠️ Always unpersist() unused datasets.

7. Real Production OOM Scenarios
7.1 Massive .collect() / .toPandas()
Problem: Driver OOM
Fix:
df.limit(1000).toPandas()


7.2 Skewed Joins
Symptoms:


Long-running tasks


High shuffle spill


Few hot partitions


Fix:


Salting


AQE


spark.sql.adaptive.enabled = true


7.3 Over-Caching
Problem: Cached datasets evict execution memory
Fix:
persist(StorageLevel.MEMORY_AND_DISK_SER)
unpersist()


7.4 Insufficient Memory Overhead (PySpark)
Symptoms:


YARN container killed


Low JVM usage


Fix:
spark.executor.memoryOverhead=6g


7.5 Broadcast Join Explosion
Problem: “Small” table becomes huge after deserialization
Fix:


Disable broadcast


spark.sql.autoBroadcastJoinThreshold = -1


7.6 Streaming State Accumulation
Problem: Unbounded state store growth
Fix:


Reduce watermark


Cleanup old state



7.7 Excessive Shuffle Partitions
Problem: Driver metadata OOM
Fix:
spark.sql.shuffle.partitions = 500


8. Golden Rules for Spark Memory
✅ Avoid .collect() on large data
✅ Tune memoryOverhead for PySpark
✅ Prefer MEMORY_AND_DISK_SER
✅ Enable AQE in Spark 3+
✅ Monitor Stages → Shuffle Spill → GC Time
✅ Unpersist aggressively
✅ Align shuffle partitions with cluster cores

9. Interview One-Liners


Spark uses Unified Memory Model


Execution memory has higher priority


Off-heap avoids GC pressure


Driver OOM ≠ Executor OOM


PySpark needs extra memoryOverhead


Cache is lazy


AQE solves skew dynamically





