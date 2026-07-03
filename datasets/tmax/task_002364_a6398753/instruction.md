As a compliance officer, I am auditing our internal transaction tracking system. We use a custom vendored Python package called `graph_auditor` to map relational compliance logs into graph structures for NoSQL aggregation and to identify cyclic transaction patterns that might indicate money laundering.

However, the `graph_auditor` package currently has a critical bug: when running concurrent audit queries, it consistently deadlocks, causing our compliance pipelines to halt. 

Your task involves two parts:
1. **Fix the Vendored Package**: The source code for `graph_auditor-1.2.0` is vendored at `/app/graph_auditor`. Investigate the package's connection and transaction handling logic. There is a deliberate flaw causing deadlocks during concurrent graph edge insertions. Identify and fix this issue directly in the vendored source code.
2. **Implement the Audit Script**: Write a Python script at `/home/user/audit.py` that uses the fixed `graph_auditor` package. The script should:
   - Accept a single JSON string as a command-line argument. This JSON string will represent an array of relational transaction records (e.g., `[{"tx_id": "T1", "from_acct": "A", "to_acct": "B", "amount": 100}, ...]`).
   - Use the package to load these records into the graph database.
   - Design and apply an optimal index strategy for the graph nodes to speed up lookups by account ID.
   - Execute a NoSQL-style aggregation pipeline (provided by the package) to find any cycles of length up to 3 involving accounts that have transacted more than $10,000 in total.
   - Print the resulting list of suspicious cycle paths (as a JSON list of lists of account IDs) to standard output.

Your script must be perfectly deterministic and equivalent to our reference implementation, as it will be rigorously tested against a fuzzing framework with thousands of random transaction sets. Ensure your code is executable as `python3 /home/user/audit.py '[{"tx_id":...}]'`.