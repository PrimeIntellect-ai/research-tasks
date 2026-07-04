You are acting as an automated system for a compliance officer auditing an internal financial network. 

We suspect that a sanctioned executive is using their downstream reporting chain to authorize obfuscated transactions. You need to trace the organizational hierarchy (a graph of management structures) and aggregate transaction amounts for all employees in that executive's subtree.

We have two data files located in `/home/user/audit_data/`:
1. `employees.json`: A JSON array of documents representing the employee graph. Each document has the schema `{"emp_id": "string", "name": "string", "manager_id": "string|null"}`. If `manager_id` is null, they are at the top of their chain.
2. `transactions.json`: A JSON array of transaction documents. Schema: `{"tx_id": "string", "emp_id": "string", "amount": float, "status": "string"}`.

Your task is to write a Python script `/home/user/audit_pipeline.py` that processes this data. The script must:
1. Accept a parameterized target manager ID as the first command-line argument (e.g., `python3 audit_pipeline.py MGR_007`).
2. Traverse the graph to find all employees who report *directly or indirectly* (at any depth) to the target manager. 
3. Perform a NoSQL-style aggregation pipeline in memory (or using a lightweight DB like DuckDB/SQLite if you prefer):
    - Filter transactions to only include those with `"status": "COMPLETED"` that belong to the identified downstream employees.
    - Group by `emp_id` and calculate the sum of the `amount` for each employee.
    - Sort the results by the total amount in descending order.
    - Paginate/limit the result to the top 3 highest transacting employees.
4. Output the final aggregated list as a JSON array to `/home/user/flagged_audit.json`. The output should look like this: `[{"emp_id": "EMP_...", "total_amount": 1250.50}, ...]`.

Once your script is written, run it against the target manager ID: `MGR_042`. Ensure the output file is generated correctly.