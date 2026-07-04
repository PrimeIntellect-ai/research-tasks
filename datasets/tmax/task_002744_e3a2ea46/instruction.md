You are an IT compliance officer auditing a financial transaction database for potential high-risk money movement chains.

You have an SQLite database located at `/home/user/financials.db`. It contains a single table:
`transfers(id INTEGER PRIMARY KEY, source TEXT, target TEXT, amount REAL)`

Your objective is to write a Bash script named `/home/user/analyze_risk.sh` that takes exactly one argument: a starting `source` account ID (e.g., `ACC1`). 

The script must execute a query against the SQLite database to perform a graph traversal and analysis. Specifically, it needs to:
1. Construct a parameterized query using the provided account ID.
2. Use a Recursive Common Table Expression (CTE) to traverse the transaction graph and find all directed paths of exact length 3 (i.e., exactly 3 consecutive transfers, involving 4 accounts, starting from the provided account ID).
3. For each valid path, calculate the `total_amount` (the sum of the amounts of the 3 transfers).
4. Construct a string representing the transfer path in the format `Source->Node1->Node2->Target` (e.g., `ACC1->ACC2->ACC3->ACC4`).
5. Use a window function (`DENSE_RANK()`) to rank the discovered paths based on their `total_amount` in descending order. The highest total amount gets rank 1.
6. Export the final results to `/home/user/risk_report.csv` as a comma-separated values file, including a header row.

The output CSV `/home/user/risk_report.csv` must exactly match this format:
```csv
rank,path,total_amount
1,ACC1->ACC5->ACC6->ACC7,560.0
...
```

Requirements:
- Ensure the script uses `#!/bin/bash`.
- The script should run the query silently and gracefully output the CSV file.
- Do not hardcode the account ID in the SQL; it must be dynamically injected via the bash script argument.