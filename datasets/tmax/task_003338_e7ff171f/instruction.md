You are assisting a compliance officer auditing an internal financial system for illicit fund flows. You have been provided with an SQLite database at `/home/user/financial_audit.db` containing two tables:
1. `accounts` (`id` INTEGER PRIMARY KEY, `name` TEXT)
2. `transfers` (`tx_id` INTEGER PRIMARY KEY, `sender_id` INTEGER, `receiver_id` INTEGER, `amount` REAL, `timestamp` INTEGER)

Write and execute a Go program at `/home/user/audit.go` that performs the following analysis:

1. **Window Function Aggregation**: Identify "flagged" transfers. A transfer is flagged if its `amount` is strictly greater than the rolling average of the current transfer and up to two preceding transfers from the *same* `sender_id` (ordered by `timestamp`). You must use a SQL Window Function to compute this directly in your database query.
2. **Graph Traversal**: Using *only* the flagged transfers, construct a directed graph where nodes are accounts and edges are transfers. Compute the shortest path (fewest number of hops) from the account named `"ShellCorp"` to the account named `"OffshoreVault"`. 
3. **Graph Analytics**: Calculate the out-degree centrality (number of outgoing edges) for all nodes in this flagged graph. Identify the account name with the highest out-degree. If there is a tie, pick the one that comes first alphabetically.
4. **Output**: Save your results in a JSON file at `/home/user/audit_result.json` with exactly this structure:
```json
{
  "shortest_path": ["ShellCorp", "NodeA", "NodeB", "OffshoreVault"],
  "highest_out_degree": "AccountName"
}
```

Constraints & Notes:
- Standard Go libraries and `github.com/mattn/go-sqlite3` are allowed.
- You may use the shell to initialize the Go module, fetch dependencies, and run your code.