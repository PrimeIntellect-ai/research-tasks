You are acting as a technical compliance officer auditing an organization's financial systems to detect potential circular transaction chains (money laundering or system deadlocks) and the users who approved them. 

You have been provided with two data sources in your home directory (`/home/user`):
1. `/home/user/transactions.ttl`: An RDF graph dataset (in Turtle format) containing financial transaction flows. 
2. `/home/user/audit_logs.db`: A SQLite database containing the access logs and approval histories.

Your task is to build a Python-based query pipeline (`/home/user/run_audit.py`) that performs the following steps:

**Phase 1: Graph Query (SPARQL)**
Write a Python script that uses the `rdflib` library to load `transactions.ttl` and execute a SPARQL query. 
Find all transaction cycles of exactly length 3. A cycle occurs when transaction A transfers to transaction B, B transfers to C, and C transfers back to A (using the `ex:transfersTo` predicate). 
Filter the cycles such that *all three* transactions in the cycle have an `ex:amount` strictly greater than `10000` (using the `ex:amount` predicate).
For the single matching cycle, sort the transaction URIs alphabetically and extract their IDs (the part after the namespace `http://example.org/tx/`). Let's call them `tx1`, `tx2`, and `tx3` where `tx1 < tx2 < tx3` alphabetically.

**Phase 2: Relational Query (SQLite)**
The SQLite database `audit_logs.db` has two tables:
- `users`: `id` (INT), `username` (VARCHAR), `department` (VARCHAR)
- `approvals`: `id` (INT), `tx_id` (VARCHAR), `user_id` (INT), `approved_at` (DATETIME)

Take the three transaction IDs (`tx1`, `tx2`, `tx3`) identified in Phase 1 and query the SQLite database to find their **most recent** approvals. 
You **must** use a single SQL query with a Window Function (e.g., `ROW_NUMBER() OVER (...)`) to find the latest approval record for each of the three transaction IDs. Join this with the `users` table to get the `username` of the approver.

**Phase 3: Pipeline Output**
Your Python script must chain these operations together automatically.
Finally, the script should write the results to a CSV file at `/home/user/audit_report.csv` with exactly the following format:
`tx1,tx2,tx3,approver1,approver2,approver3`

Where `approver1` is the username who made the latest approval for `tx1`, `approver2` for `tx2`, etc.

Requirements:
- Install any necessary Python packages (like `rdflib`) using `pip`.
- Run your script and ensure `/home/user/audit_report.csv` is generated successfully.
- Do not use any external graph databases; do it purely via Python and `rdflib`.