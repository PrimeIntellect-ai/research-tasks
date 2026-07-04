You are a data engineer debugging an ETL pipeline that routinely deadlocks due to complex concurrent resource requests. We have captured the event logs in a SQLite database. Your task is to extract this data, transform it into a graph representation, and identify the deadlocks.

The database is located at `/home/user/transaction_logs.db`.
It has a single table:
`events(event_id INTEGER, tx_id TEXT, resource_id TEXT, action TEXT, event_time INTEGER)`

The `action` column contains either `'HOLD'`, `'WAIT'`, or `'RELEASE'`. 
* `'HOLD'` means the transaction successfully acquired the resource.
* `'WAIT'` means the transaction is currently waiting to acquire the resource.
* `'RELEASE'` means the transaction has released the resource.

A transaction might wait for a resource, acquire it later, and then release it. To find the *current* state of the system, you must use a SQL analytical/window function to determine the *latest* action for every `(tx_id, resource_id)` pair based on `event_time`. Ignore any pair where the latest action is `'RELEASE'`.

Next, build a Wait-For Graph (WFG) in Python. 
* The nodes in the graph are the transactions (`tx_id`).
* A directed edge exists from Transaction A to Transaction B if Transaction A's latest state for a resource is `'WAIT'`, and Transaction B's latest state for that *same* resource is `'HOLD'`.

Find all deadlocks in this system. A deadlock is defined as a simple cycle in the Wait-For Graph.

Output the result to `/home/user/deadlocks.json`. The output must perfectly validate against this JSON structure:
```json
{
  "deadlocks": [
    ["TxA", "TxB"],
    ["TxC", "TxD", "TxE"]
  ]
}
```

Constraints for the output:
1. Each inner list represents one cycle (deadlock).
2. The `tx_id`s inside each cycle list must be sorted alphabetically.
3. The outer `deadlocks` list must be sorted alphabetically based on the first element of each inner list.
4. Each distinct cycle should only be listed once.