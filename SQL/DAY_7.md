Goal: Think like a senior engineer Concepts • Index basics • Composite indexes • Query execution order • EXPLAIN • Common performance killers Interview Questions • Why index not used? • Clustered vs non-clustered index • When full table scan is faster Practice • Rewrite slow queries • Add correct indexes • Read EXPLAIN output Must-Know Trap Functions on indexed columns break index usage

>>Index Basics
>>Composite Indexes
>>Query Execution Order
>>EXPLAIN
 >| Column  | Meaning       |
| ------- | ------------- |
| `type`  | Access method |
| `key`   | Index used    |
| `rows`  | Rows scanned  |
| `Extra` | Warnings      |

>>Common Performance Killers
>>Practice: Rewrite Slow Query
Before approving a query:

✅ Does EXPLAIN avoid ALL?
✅ Index matches WHERE + JOIN order?
✅ No functions on indexed columns?
✅ Composite index follows left-most rule?
✅ Rows scanned ≪ rows returned?