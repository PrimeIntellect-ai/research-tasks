You are an AI assistant helping a compliance officer audit an internal financial system for potential money laundering and unauthorized access patterns. 

You have been provided with a dataset at `/home/user/transactions.csv` containing raw transaction logs. The CSV has the following columns:
`tx_id,timestamp,source_account,target_account,amount`
(Note: `timestamp` is a Unix epoch integer, `amount` is a double/float, others are strings).

Your task is to write a C++ program at `/home/user/audit_analyzer.cpp` that processes this data to identify compliance violations. Your solution must use the SQLite3 C/C++ interface (`sqlite3.h`) to load, index, and analyze the data.

The compliance officer requires you to perform the following:
1. **Database & Indexing:** Load the CSV data into an in-memory SQLite database. You must design and execute an index strategy (using `CREATE INDEX` statements) that optimizes the subsequent analytical and graph queries.
2. **Analytical Aggregation (Window Functions):** Identify all "Suspicious Accounts". A suspicious account is any `source_account` that has a rolling sum of outgoing `amount` >= 50,000.0 within any 24-hour (86400 seconds) window. Use SQLite's window functions (`OVER`, `PARTITION BY`, `ORDER BY`, `RANGE BETWEEN`) to calculate this.
3. **Graph Materialization:** Using the identified Suspicious Accounts as seed nodes, project a graph of transactions to find circular money flows. Specifically, find all cycles of exactly length 3 (A -> B -> C -> A) where account 'A' is a Suspicious Account. The edges in this graph are the transactions from the dataset.
4. **Reporting:** Export the results to `/home/user/audit_report.json` in the following exact JSON format:
```json
{
  "suspicious_accounts": ["ACC123", "ACC456"],
  "cycles": [
    ["ACC123", "ACC999", "ACC888"]
  ]
}
```
*Note: Sort the `suspicious_accounts` alphabetically. For `cycles`, ensure the cycle array starts with the Suspicious Account, and sort the list of cycles lexicographically based on the JSON string representation of the array.*

**System Requirements:**
*   You must compile your program using standard C++17 (e.g., `g++ -std=c++17 /home/user/audit_analyzer.cpp -lsqlite3 -o /home/user/audit_analyzer`).
*   You may need to install the SQLite3 development headers first (e.g., `sudo apt-get update && sudo apt-get install -y libsqlite3-dev`). Note: You can use `sudo` for `apt-get` but your script will run as the standard `user`.
*   Run the compiled executable to generate the report.