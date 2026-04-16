## SNS, SQS, and EventBridge

### 1) What is the service purpose?
- `SNS (Simple Notification Service)`: Pub/sub messaging. One publisher sends a message to a topic, and SNS fan-outs to many subscribers (SQS, Lambda, HTTP, email, etc.).
- `SQS (Simple Queue Service)`: Durable message queue for decoupling services and buffering load. Consumers pull/process messages asynchronously.
- `EventBridge`: Event bus for routing events from AWS services, custom apps, and SaaS. Uses rules to match event patterns and route to targets.

### 2) Where used in real-world scenarios?
- Order processing: app publishes `OrderCreated` event, then inventory, billing, and shipping consume independently.
- Notifications: SNS topic fans out alerts to email/SMS/Lambda/SQS.
- Microservices decoupling: SQS between services to absorb traffic spikes and improve reliability.
- Event-driven automation: EventBridge rule reacts to AWS events (for example, EC2 state change) and triggers Lambda/Step Functions.
- Audit/integration: EventBridge forwards selected events cross-account or to a central observability account.

### 3) Internal working
- `SNS`:
  - Producer publishes to a topic.
  - SNS stores/retries delivery per protocol.
  - For SQS subscribers, SNS pushes messages into queues.
- `SQS`:
  - Producer sends message to queue.
  - Queue stores redundantly across AZs.
  - Consumer polls, processes, and deletes message.
  - If not deleted before visibility timeout, message becomes visible again.
  - Optional DLQ captures poison messages after max receives.
- `EventBridge`:
  - Event source sends JSON event to bus.
  - Rules evaluate event pattern.
  - Matching rules invoke targets (Lambda, SQS, SNS, Step Functions, etc.).
  - Supports retries, DLQ (for some targets), archive/replay.

### 4) Interview questions (with short answers)
1. Difference between SNS and SQS?
   - SNS is push-based pub/sub fan-out; SQS is pull-based queue for one consumer group.
2. When do you combine SNS + SQS?
   - When one event must go to multiple independent consumers with buffering and retry isolation.
3. Standard vs FIFO SQS?
   - Standard: high throughput, at-least-once, best-effort ordering. FIFO: exactly-once processing (with dedup), strict ordering, lower throughput.
4. What is visibility timeout in SQS?
   - Time a received message is hidden from other consumers; prevents duplicate parallel processing.
5. Why use DLQ?
   - Isolate repeatedly failing messages for debugging and to keep main queue healthy.
6. EventBridge vs SNS?
   - EventBridge supports rich event filtering/routing and schema-based event buses; SNS focuses on simple pub/sub fan-out.
7. How to secure these services?
   - IAM least privilege, resource policies, encryption (KMS), private endpoints, and access condition keys.

### 5) One demo to get hands-on
Build: `EventBridge -> SNS Topic -> SQS Queue -> Lambda Consumer`

Steps:
1. Create an SQS queue: `orders-queue` (+ optional `orders-dlq`).
2. Create SNS topic: `orders-topic`.
3. Subscribe `orders-queue` to `orders-topic`.
4. Add SQS queue policy allowing SNS topic to send messages.
5. Create EventBridge custom bus (or use default) and rule:
   - Pattern: `{ "source": ["demo.orders"], "detail-type": ["OrderCreated"] }`
   - Target: SNS topic `orders-topic`.
6. Put a test event from EventBridge:
   - source: `demo.orders`
   - detail-type: `OrderCreated`
   - detail: `{ "orderId": "123", "amount": 499 }`
7. Verify message reaches SQS.
8. Attach Lambda trigger to SQS and log processed payload to CloudWatch.

Expected outcome:
- One event published once.
- Fan-out/routing works through EventBridge + SNS.
- Queue buffers message until consumer processes it.

### 6) Limits (default and scalable values)
`Note:` Quotas are region-specific and can change. Values below are the common defaults from AWS docs (checked on March 6, 2026).

#### SNS
| Limit | Default value | Scalable / max behavior |
|---|---|---|
| Publish throughput (messages/sec, per account, per Region) | Example: `us-east-1 = 30,000`, `us-west-2/eu-west-1 = 9,000`, many Regions `1,500` or `300` | Soft limit, can request increase in Service Quotas |
| Subscribers per topic | Standard: `12,500,000`; FIFO: `100` | Topic/subscription quotas can be increased where AWS allows |
| FIFO topic throughput | `3,000 msg/sec` per topic (`or 20 MB/sec`, whichever first) when `FifoThroughputScope=Topic`; `300 msg/sec` per message group | Scales via message-group parallelism and quota increase requests |
| Message size | Up to `256 KB` payload (larger payload pattern uses S3 pointer) | Hard service limit for direct payload |
| Message lifetime/retention | SNS is not a queue; no user-set queue-style retention | Delivery retries depend on protocol; use SQS if you need retention/buffering |

#### SQS
| Limit | Default value | Scalable / max behavior |
|---|---|---|
| Message retention | Default `4 days` | Configurable `1 minute` to `14 days` |
| Visibility timeout | Default `30 seconds` | Configurable `0 seconds` to `12 hours` |
| Standard queue throughput | Very high / nearly unlimited API TPS | Auto-scales; use multiple consumers/queues for extreme scale |
| FIFO throughput (non-high-throughput mode) | `300 TPS` per API action; with batching up to `3,000 msg/sec` | High-throughput FIFO mode increases to region-based maxima |
| FIFO high-throughput (example Regions) | Up to `70,000 TPS` non-batched (`700,000 msg/sec` batched) in top Regions | Region-dependent (for example 19k/9k/4.5k/2.4k TPS in other Regions) |
| In-flight messages | ~`120,000` standard; `120,000` FIFO | Standard is adjustable; FIFO increases via AWS Support |
| Queue backlog size | Unlimited stored messages | Practically bounded by cost and processing capacity |
| Message size | Up to `1 MiB` | For larger payloads, store body in S3 and send pointer |

#### EventBridge
| Limit | Default value | Scalable / max behavior |
|---|---|---|
| PutEvents throughput (TPS, per account, per Region) | Example: `us-east-1/us-west-2/eu-west-1 = 10,000`; many Regions lower | Adjustable in Service Quotas |
| Rule invocations throughput (TPS) | Example: up to `18,750` in top Regions | Adjustable in Service Quotas (throttled/delayed when exceeded) |
| Rules per event bus | Usually `300` per bus (`100` in some Regions) | Adjustable |
| Targets per rule | `5` | Hard limit per rule |
| Event size | `256 KB` per event entry | Hard limit (use S3 reference pattern for large payload data) |
| Event lifetime on bus | Event bus is not a queue; no queue-style retention by default | Target delivery retries: default `24 hours` and up to `185` attempts |
| Archive retention (optional) | Default indefinite when archive is enabled | Set retention days as needed; replay supported |

