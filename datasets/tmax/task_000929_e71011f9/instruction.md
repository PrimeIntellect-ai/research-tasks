You are assisting a compliance officer auditing an international corporate network. The company has a legacy compliance tool located at `/app/legacy_auditor` (a stripped executable binary). This tool analyzes corporate ownership structures and transactions to flag potential "self-dealing" compliance violations. However, the legacy tool is notoriously buggy: due to a flawed internal SQL query involving an implicit cross-join, it generates massive amounts of false positives, effectively flagging almost any transaction over a certain amount.

Your task is to write a Python CLI tool at `/home/user/compliance_filter.py` that implements the correct auditing logic, acting as a strict filter for transactions. 

The corporate data is stored in a SQLite database located at `/app/data/corp.db` with the following tables:
- `entities (id INTEGER PRIMARY KEY, name TEXT)`
- `ownership (parent_id INTEGER, child_id INTEGER)`

Your Python script must evaluate individual transaction files (in JSON format) and determine if they are compliant.
The script must accept two arguments:
`python3 /home/user/compliance_filter.py --db <path_to_db> --tx <path_to_tx_json>`

A transaction JSON looks like this:
`{"tx_id": "tx_102", "sender_id": 4, "receiver_id": 9, "amount": 65000.0}`

**Compliance Rules:**
A transaction is considered a **VIOLATION** (and must be rejected) if and only if BOTH of the following conditions are met:
1. The transaction `amount` is strictly greater than `50000.0`.
2. The `sender_id` and `receiver_id` belong to the same "corporate cluster". A corporate cluster is defined as a connected component in the `ownership` graph, treating all ownership edges as *undirected*. You will likely need to use recursive CTEs or a graph analytics library in Python (like `networkx`) to project the graph and evaluate paths.

**Expected Behavior:**
- If the transaction is a VIOLATION, the script must terminate with exit code `1` (Reject).
- If the transaction is COMPLIANT, the script must terminate with exit code `0` (Accept).

You must ensure your script handles complex, deep ownership hierarchies efficiently. You can analyze `/app/legacy_auditor` to see how it fails, but your primary goal is to write a robust Python script that correctly enforces the rules above.