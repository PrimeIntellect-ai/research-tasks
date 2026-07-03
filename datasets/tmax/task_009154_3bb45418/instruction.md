You are acting as a compliance officer auditing a distributed database system. Recently, the system has experienced severe slowdowns, and the engineering team suspects distributed deadlocks are occurring. They have provided you with a snapshot of the lock table across all nodes.

Your task is to analyze the lock data, construct a wait-for graph, detect all deadlocks (cycles), and generate a summary report.

**Task Details:**
1. **Data Location**: The lock data is located at `/home/user/audit_data/locks.csv`. 
2. **Data Model**: The CSV has four columns: `transaction_id`, `resource_id`, `status`, and `timestamp`.
   - `status` is either `GRANTED` (the transaction holds the lock on the resource) or `WAITING` (the transaction is blocked, waiting to acquire the lock).
   - *Note on Wait-For Graph*: A transaction $T_A$ is "waiting for" transaction $T_B$ if $T_A$ is `WAITING` on a resource that is currently `GRANTED` to $T_B$.
3. **Graph Processing**:
   - Construct a directed Wait-For graph of transactions based on the rules above. Note that resources are not nodes in the final Wait-For graph; the edges are strictly Transaction -> Transaction.
   - Detect all deadlocks in this system. A deadlock is defined as any simple cycle in the directed Wait-For graph.
4. **Aggregation & Export**:
   - For every transaction, count the total number of distinct simple cycles it is a part of.
   - Export this data to a JSON file at `/home/user/deadlock_report.json`.
   - The JSON must be a single flat dictionary mapping the `transaction_id` (as a string) to the integer count of cycles it participates in. 
   - *Only* include transactions that are involved in at least 1 cycle. Do not include transactions with 0 cycles.

**Example Output Format:**
```json
{
  "T1": 1,
  "T2": 1,
  "T7": 2
}
```

You may use any programming language (e.g., Python, Node.js) or database tool (e.g., SQLite, DuckDB) available or installable in your environment to process this data. Ensure your solution is exact and handles the specified format precisely.