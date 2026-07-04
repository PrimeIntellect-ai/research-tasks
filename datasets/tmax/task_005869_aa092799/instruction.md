You are acting as a compliance officer auditing an organization's internal IT systems. Recent policy changes require strict auditing of access to highly sensitive corporate assets.

You have been provided with an SQLite database at `/home/user/iam_graph.db` which acts as a rudimentary Knowledge Graph of the organization's Identity and Access Management (IAM) system. 

The database contains two tables representing a directed graph:
1. `nodes`: Contains `id` (integer), `type` (text: 'USER', 'ROLE', or 'ASSET'), and `name` (text).
2. `edges`: Contains `source_id` (integer), `rel_type` (text: 'HAS_ROLE', 'INHERITS', 'CAN_READ', 'CAN_WRITE'), and `target_id` (integer).

**Your Objective:**
We need to identify all users who have `WRITE` access to the asset named `FINANCIAL_LEDGER`. 

In our IAM model, a user has `WRITE` access to an asset if and only if there is a path in the graph matching this exact pattern:
1. A 'USER' node is connected to a 'ROLE' node via a `HAS_ROLE` edge.
2. That 'ROLE' node connects to another 'ROLE' node via zero or more `INHERITS` edges (meaning a role can inherit from another role, which inherits from another, etc.).
3. The final 'ROLE' node in that inheritance chain connects to the 'ASSET' node via a `CAN_WRITE` edge.

**Tasks:**
1. Analyze the schema and relationships in `/home/user/iam_graph.db`.
2. Write a Python script at `/home/user/audit_script.py` that queries this database to find all users matching the exact authorization pattern described above for the `FINANCIAL_LEDGER` asset. You may use SQLite recursive Common Table Expressions (CTEs) or graph libraries (e.g., `networkx`) to resolve the hierarchical role inheritance.
3. The script must execute and write the final list of authorized user names to a file at `/home/user/flagged_users.txt`.
4. The output file `/home/user/flagged_users.txt` must contain exactly one username per line, sorted alphabetically. Do not include any headers, footers, or extra text in this file.

Ensure your script is self-contained and produces the expected output file when run.