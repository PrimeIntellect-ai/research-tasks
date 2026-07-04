You are acting as a technical compliance officer auditing financial transaction networks. Your goal is to develop a Python-based compliance detector that flags evasive money-laundering topologies (specifically, structured circular funding and unauthorized entity paths). 

You have been provided a pre-vendored version of the `networkx` library located at `/app/networkx-source`. We have observed that scripts relying on this local package for shortest-path calculations are yielding off-by-one errors in their depth cutoffs, causing false negatives in our audits. 

Your tasks are:

1. **Fix the Vendored Package:**
   Investigate and patch the local `/app/networkx-source` package so that standard shortest-path algorithms function correctly. Ensure your Python environment is using this local package (e.g., via `PYTHONPATH`).

2. **Develop the Audit Detector:**
   Write a Python script at `/home/user/detector.py` that processes a given SQLite database file and determines if it represents a compliance violation.
   
   The database contains a single table `transactions` with columns: `id`, `source_account`, `target_account`, `amount`, `timestamp`.
   
   A database should be flagged as a violation (output "EVIL") if IT MEETS BOTH of the following conditions, otherwise it should be cleared (output "CLEAN"):
   - **Condition A (SQL Analytical Aggregation):** The database contains at least one account that has conducted more than 3 outgoing transactions within any rolling 24-hour window, where the sum of those transactions in that window exceeds $50,000. You must determine this using SQL window functions.
   - **Condition B (Graph Traversal):** By constructing a directed graph of all transactions (ignoring amounts and timestamps), there exists a directed path from any account starting with the prefix `SANCTIONED_` to any account starting with the prefix `CLEARED_` in 3 hops or fewer.
   
   Your script must take a single command-line argument (the path to the SQLite DB) and print exactly "EVIL" or "CLEAN" to standard output.

3. **Verify Against the Corpora:**
   Test your detector against the compliance corpora located at `/home/user/corpora/evil/` and `/home/user/corpora/clean/`. Your detector must correctly reject 100% of the evil databases and accept 100% of the clean databases.