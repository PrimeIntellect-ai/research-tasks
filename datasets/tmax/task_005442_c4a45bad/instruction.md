You are an AI assistant helping a database researcher organize and analyze a dataset of concurrent transactions to identify system deadlocks.

A SQLite database is located at `/home/user/transactions.db`. It contains three tables capturing the state of transactions and their resource locks:
1. `transactions` (`tx_id` INTEGER, `status` TEXT) - Status can be 'ACTIVE' or 'ABORTED'.
2. `locks_held` (`tx_id` INTEGER, `resource_id` INTEGER) - Represents resources currently locked by a transaction.
3. `locks_waiting` (`tx_id` INTEGER, `resource_id` INTEGER) - Represents resources a transaction is requesting but are currently locked by someone else.

Your task is to analyze this data to find transaction deadlocks (circular dependencies) using SQL and Python. 
A "waits-for" directed edge exists from Transaction A to Transaction B if A is waiting for a resource that B currently holds.

Requirements:
1. **Filter**: Only consider transactions with an 'ACTIVE' status. Completely ignore 'ABORTED' transactions in all your graph building and calculations.
2. **Graph Construction**: Construct the "waits-for" directed graph (A -> B).
3. **Deadlock Detection**: Identify all deadlocks. A deadlock is defined as a Strongly Connected Component (SCC) in the waits-for graph that contains more than 1 node.
4. **Graph Analytics**: Among all the transactions that are involved in *any* deadlock, identify the `most_blocking_tx`. This is the transaction with the highest in-degree (number of incoming wait-for edges) in the *entire* active graph. If there is a tie, pick the one with the smallest `tx_id`.
5. **Pagination**: Extract all the "waits-for" edges that exist strictly *between* nodes that are part of the deadlocks (i.e., if A and B are both in the set of deadlocked nodes, and A->B exists, include it). Sort these edges ascending first by the waiter's `tx_id`, then by the holder's `tx_id`. Paginate this sorted list with exactly 2 edges per page.
6. **Output**: Write your final results to `/home/user/deadlock_report.json` exactly matching this schema:
```json
{
  "deadlocked_transactions": [101, 102, 103], /* Flat, sorted list of all tx_ids involved in any deadlock */
  "clusters": [[101, 102], [104, 105]], /* Sorted list of sorted lists, each inner list is a deadlock SCC */
  "most_blocking_tx": 102, /* Integer tx_id of the most blocking transaction in the deadlocked set */
  "paginated_edges": {
    "page_1": [{"waiter": 101, "holder": 102}, {"waiter": 102, "holder": 103}],
    "page_2": [{"waiter": 103, "holder": 101}]
  }
}
```

Constraints:
- You must use Python to perform the graph analytics and JSON generation. You may use standard libraries and `networkx`. If `networkx` is not installed, install it.
- Ensure your JSON keys and structures perfectly match the requested schema.