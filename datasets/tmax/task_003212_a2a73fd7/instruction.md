You are an AI assistant helping a compliance officer audit a corporate financial system. We suspect that certain accounts are engaged in money laundering via circular transactions, but our initial queries have returned inconsistent results. 

We have isolated the transaction records in an SQLite database located at `/home/user/finances.db`. The database contains a single table:
`transactions (id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, amount REAL, tx_date DATETIME)`

The compliance officer noted that the database index `idx_sender` was corrupted during a recent system crash, causing queries to return stale or missing rows. 

Your task is to write and execute a Python script (`/home/user/audit_pipeline.py`) that performs the following end-to-end data processing pipeline:

1. **Database Repair & Querying:** Connect to the SQLite database. You must first execute the appropriate SQL command to rebuild the corrupted indexes. 
2. **Analytical Aggregation (Window Functions):** Construct a parameterized SQL query that uses window functions to identify "High Risk" senders. A sender is considered "High Risk" if the moving average of their `amount` over their *last 3 transactions* (partitioned by `sender`, ordered by `tx_date` ascending, examining the current row and the 2 preceding rows) strictly exceeds $50,000.
3. **Graph Materialization:** Query all transactions from the database and project them into a directed graph using `networkx`, where nodes are accounts (senders/receivers) and directed edges represent a transaction from a sender to a receiver.
4. **Knowledge Graph Pattern Matching:** Analyze the graph to find all directed cycles of exactly length 3 (i.e., A -> B -> C -> A). 
5. **Cross-Referencing:** Filter these cycles to find only the ones where *at least one* node in the cycle belongs to the "High Risk" senders identified in step 2.

**Expected Output:**
Your script must write the results to `/home/user/compliance_report.json`. The JSON file should contain a list of lists. Each inner list should contain the account names (strings) involved in a flagged cycle. 
- The account names within each inner list must be sorted alphabetically.
- The outer list must be sorted lexicographically based on the inner lists.

Example output format:
`[["AccountA", "AccountB", "AccountC"], ["AccountX", "AccountY", "AccountZ"]]`

You may install any required Python packages (e.g., `networkx`, `pandas`) using pip. Use standard Python 3.