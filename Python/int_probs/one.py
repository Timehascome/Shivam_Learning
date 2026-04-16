"""
Python Screening Problem: Transaction Deduplication and Daily Exposure

Context:
You are working as a Lead Data Engineer for a fintech platform. Raw transaction
events arrive from multiple upstream systems, and duplicate records are common
because of retries, batch replays, and delayed ingestion. The business wants a
clean daily exposure report per account.

Problem Statement:
Given a list of transaction records, write a function:

    def daily_net_exposure(transactions: list[dict]) -> dict:

that returns the net transaction amount per account per day after removing
duplicates.

Each transaction dictionary contains:
- "txn_id": unique transaction identifier from source system
- "account_id": account number as a string
- "amount": signed numeric amount
- "event_time": timestamp string in the format "YYYY-MM-DD HH:MM:SS"

Deduplication Rules:
1. Records with the same "txn_id" are duplicates of the same business event.
2. Keep only the record with the latest "event_time" for each "txn_id".
3. After deduplication, group records by:
   - transaction date (YYYY-MM-DD extracted from "event_time")
   - account_id
4. Compute the net sum of "amount" for each (date, account_id) pair.

Return Format:
Return a dictionary in this form:

{
    "2026-03-18": {
        "A101": 1300,
        "B205": -200
    },
    "2026-03-19": {
        "A101": 500
    }
}

Example Input:
transactions = [
    {"txn_id": "T1", "account_id": "A101", "amount": 1000, "event_time": "2026-03-18 09:00:00"},
    {"txn_id": "T2", "account_id": "A101", "amount": 300,  "event_time": "2026-03-18 10:30:00"},
    {"txn_id": "T1", "account_id": "A101", "amount": 1000, "event_time": "2026-03-18 09:05:00"},
    {"txn_id": "T3", "account_id": "B205", "amount": -200, "event_time": "2026-03-18 11:00:00"},
    {"txn_id": "T4", "account_id": "A101", "amount": 500,  "event_time": "2026-03-19 08:15:00"}
]

Expected Output:
{
    "2026-03-18": {
        "A101": 1300,
        "B205": -200
    },
    "2026-03-19": {
        "A101": 500
    }
}

Follow-up Questions Often Asked in Screening Rounds:
1. What is the time and space complexity of your solution?
2. How would you handle invalid timestamps or missing fields?
3. How would this design change if the input size is too large to fit in memory?
4. How would you extend this for Spark or Pandas pipelines?

Why this is relevant:
- Tests dictionary/hashmap usage
- Tests sorting or timestamp comparison logic
- Reflects real-world fintech data engineering problems
- Opens discussion on scalability, data quality, and production design
"""

from datetime import datetime
from collections import defaultdict 

def daily_net_exposure(transactions: list[dict]) -> dict:
    latest_txn = {}
    for txn in transactions:
        if txn['txn_id'] not in latest_txn or datetime.strptime(txn['event_time'], "%Y-%m-%d %H:%M:%S")> datetime.strptime(latest_txn[txn['txn_id']]['event_time'], "%Y-%m-%d %H:%M:%S"):
            latest_txn[txn['txn_id']] = txn
    exposure={}     
    for txn in latest_txn.values():
        date = txn['event_time'][:10]
        account_id = txn['account_id']
        amount = txn['amount']
        if date not in exposure:
            exposure[date] = defaultdict(int)
        exposure[date][account_id] += amount
    return {date: dict(accounts) for date, accounts in exposure.items()}
  



res=daily_net_exposure([
    {"txn_id": "T1", "account_id": "A101", "amount": 1000, "event_time": "2026-03-18 09:00:00"},
    {"txn_id": "T2", "account_id": "A101", "amount": 300,  "event_time": "2026-03-18 10:30:00"},
    {"txn_id": "T1", "account_id": "A101", "amount": 1000, "event_time": "2026-03-18 09:05:00"},
    {"txn_id": "T3", "account_id": "B205", "amount": -200, "event_time": "2026-03-18 11:00:00"},
    {"txn_id": "T4", "account_id": "A101", "amount": 500,  "event_time": "2026-03-19 08:15:00"}
])

print(res)