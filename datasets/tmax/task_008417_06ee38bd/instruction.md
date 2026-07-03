You are acting as a compliance officer auditing an internal financial system for illicit activities. 

You have been given access to two data sources:
1. An SQLite database containing transaction records: `/home/user/data/finance.db`
2. A JSON document containing employee communication logs: `/home/user/data/comms.json`

Because of a known system bug simulating a "corrupted index", the `transactions` table in the database contains stale rows. Specifically, some transactions that were deleted are still present in the `transactions` table. You must cross-reference the `transactions` table with the `audit_log` table to determine the true state of a transaction.

Your task is to identify the central figures involved in suspicious activities by following these steps:

1. **Identify Active Flagged Transactions:**
   Query the `finance.db` database to find all transactions where `status = 'flagged'`. However, you must exclude any transactions that have an action of `'deleted'` in the `audit_log` table (which tracks `tx_id`, `action`, and `timestamp`). Assume a transaction is deleted if its *latest* `audit_log` entry is `'deleted'`.

2. **Extract Suspicious Entities:**
   Compile a unique list of all employees (both `sender` and `receiver`) involved in these *active* flagged transactions.

3. **Build a Communication Subgraph:**
   Parse `/home/user/data/comms.json`. Filter the communications to only include records where *both* the `source` and `target` employees are in your list of suspicious entities. Treat these communications as a directed graph.

4. **Compute Centrality:**
   Using Python and the `networkx` library, build a directed graph from the filtered communications. Calculate the PageRank of the nodes in this subgraph using the default `networkx.pagerank()` parameters.

5. **Generate Report:**
   Write the top 3 employee IDs with the highest PageRank scores to `/home/user/report.txt`. 
   The file should have exactly three lines, formatted as:
   `employee_id: score`
   Round the score to 4 decimal places. Sort in descending order of the score. If there is a tie, sort alphabetically by `employee_id`.

You can install any necessary Python packages (e.g., `networkx`, `pandas`) using pip.