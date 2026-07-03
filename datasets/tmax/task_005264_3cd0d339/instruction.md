You are acting as a technical compliance officer auditing a financial platform's database. Your goal is to detect potential money laundering rings by finding specific cyclical transfer patterns, and to recommend a database optimization that prevents read/write deadlocks during concurrent compliance checks.

The system uses a SQLite database located at `/home/user/transactions.db`. It contains a table named `transfers` which logs financial movements between accounts.

Your tasks:
1. Write a Python script at `/home/user/find_cycles.py` that connects to the database, queries the `transfers` table, and finds all distinct account cycles of exactly length 4. A cycle of length 4 means there are exactly 4 distinct accounts (A, B, C, D) such that A transferred to B, B transferred to C, C transferred to D, and D transferred to A. 
2. The script must output these cycles to a log file at `/home/user/cycles.log`. Each line in the log file must represent one cycle, formatted as a comma-separated list of the 4 account IDs sorted in ascending numerical order (e.g., `1,2,3,4`). The lines in the file must also be sorted numerically.
3. To prevent full table scans that have been causing locking issues with concurrent transactions, create an SQL script at `/home/user/optimize.sql` containing a single `CREATE INDEX` statement. This index should be designed to optimize queries that traverse the graph by matching `sender_id` and `receiver_id`.

Note: 
- An account cannot transfer to itself in these cycles, and all 4 accounts in a cycle must be distinct.
- Ensure the Python script creates the output file `/home/user/cycles.log` when executed.