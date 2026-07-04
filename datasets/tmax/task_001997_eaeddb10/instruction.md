You are a data analyst investigating a severe database outage caused by distributed deadlocks. The engineering team has provided you with transaction logs exported as multiple CSV files. 

Your task is to parse these logs, reconstruct the "wait-for" dependency graph of the transactions, perform graph analytics to identify the deadlocks and the most critical bottleneck transaction, and output the results in a strictly validated JSON format.

**Data Information:**
The logs are located at `/home/user/data/log_part1.csv` and `/home/user/data/log_part2.csv`.
Each CSV has the following columns: `timestamp`, `tx_id`, `resource_id`, `action`
*   `action` can be `ACQUIRE`, `REQUEST`, or `RELEASE`.
*   A transaction holds a resource if it successfully executed an `ACQUIRE` (and hasn't executed a `RELEASE` for it).
*   A transaction is "waiting for" another transaction if it logs a `REQUEST` for a resource that is currently *held* by the other transaction. This creates a directed edge in the wait-for graph: `tx_id (waiting) -> tx_id (holding)`.

**Task Steps:**
1. You may install Python packages like `pandas` and `networkx` as needed.
2. Combine and sort all log entries chronologically by `timestamp`.
3. Process the events sequentially to build the final state of the directed wait-for graph (who is waiting for whom at the very end of the logs). Note: A transaction stops holding a resource when it logs a `RELEASE`.
4. Using graph analytics, find all simple cycles in the directed graph (each cycle represents a deadlock).
5. Calculate the Betweenness Centrality for all nodes in the directed graph to find the transaction that acts as the biggest bottleneck.
6. Generate a JSON report at `/home/user/deadlock_report.json` with the following schema:
   ```json
   {
     "deadlocks": [
       ["T1", "T2", "T3"],
       ...
     ],
     "bottleneck_tx": "T_ID",
     "bottleneck_centrality": 0.0
   }
   ```
   **Output Constraints:**
   *   For the `deadlocks` list: Sort the transaction IDs within each cycle alphabetically. Then, sort the list of cycles themselves alphabetically based on their first element (and subsequent elements if tied).
   *   `bottleneck_tx` should be the `tx_id` with the highest betweenness centrality. If there's a tie, pick the one that comes first alphabetically.
   *   `bottleneck_centrality` should be rounded to 4 decimal places.

Work entirely within `/home/user/`. Ensure your final JSON precisely matches the structure described.