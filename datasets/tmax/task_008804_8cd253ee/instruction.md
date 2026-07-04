You are a compliance officer investigating a severe database outage caused by concurrent transaction deadlocks. 

You have been given access to an undocumented SQLite database file located at `/home/user/audit.db`. This database contains raw logs of database locks requested by different process IDs (PIDs) leading up to the crash.

Your objective is to reverse-engineer the schema, reconstruct the lock dependency graph, identify the deadlocks, and find the bottleneck transactions.

Perform the following tasks:
1. Reconstruct the dependency graph: A transaction (PID A) is "waiting" on another transaction (PID B) if PID A has a 'WAITING' status for a resource that PID B currently has 'GRANTED'. This creates a directed edge from PID A to PID B.
2. Analyze the graph:
   - Identify the PIDs involved in a deadlock cycle. 
   - Calculate the PageRank of all PIDs in this directed dependency graph (use NetworkX's default PageRank implementation in Python: `nx.pagerank(G)`).
3. Analyze resource hoarding using a Window Function:
   - Using a SQL window function, calculate the rank of each PID based on the total number of 'GRANTED' locks it holds. Rank them in descending order of their granted lock count. If there's a tie, rank the smaller PID number higher (i.e., `ORDER BY count DESC, pid ASC`).

Finally, output your findings to a JSON file at `/home/user/report.json` with the following exact structure:
```json
{
  "deadlock_cycle_pids": [list of PIDs in the cycle, sorted in ascending numerical order],
  "highest_pagerank_pid": integer_pid_with_highest_pagerank,
  "top_ranked_hoarder_pid": integer_pid_with_rank_1_from_window_function
}
```

Constraints & Notes:
- You must use Python (e.g., `sqlite3`, `networkx`, `pandas`) to solve this.
- If there are multiple disconnected cycles, include the PIDs from the cycle that involves the PID with the highest PageRank. (In this dataset, there is only one cycle).