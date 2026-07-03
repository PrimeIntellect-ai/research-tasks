You are a compliance officer auditing a company's internal communication network for unauthorized information bottlenecks. The communication data is stored in an SQLite database at `/home/user/audit.db`. 

During a previous system crash, the index `idx_sender` on the `communications` table became corrupted. Simple `SELECT` queries that utilize this index return stale or missing rows. 

Your task is to write a Python script at `/home/user/audit_graph.py` that performs the following:
1. Connects to `/home/user/audit.db`.
2. Queries the `communications` table (columns: `sender_id`, `receiver_id`) while explicitly bypassing the corrupted index using SQLite's `NOT INDEXED` clause to ensure all rows are retrieved.
3. Uses the `networkx` library to build a directed graph from the retrieved records (`sender_id` -> `receiver_id`).
4. Calculates the **in-degree centrality** of all nodes in the network.
5. Sorts the results and exports the top 3 most central employees (highest in-degree centrality) to `/home/user/central_actors.json` in the following format:
```json
[
  {"employee_id": "EMP123", "centrality": 0.15},
  {"employee_id": "EMP005", "centrality": 0.12},
  {"employee_id": "EMP099", "centrality": 0.08}
]
```
(Note: centralities should be rounded to 4 decimal places).

Ensure your script runs successfully and produces the exact JSON format specified. You may use any standard Python libraries as well as `networkx`.