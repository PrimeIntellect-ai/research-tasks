You are acting as a technical assistant for a compliance officer auditing an internal corporate network for illicit information flow. 

You have been given access to a SQLite database located at `/home/user/audit.db`. This database contains two tables:
1. `employees` (`id` INTEGER, `name` TEXT, `department` TEXT)
2. `communications` (`sender_id` INTEGER, `receiver_id` INTEGER, `timestamp` DATETIME)

There is a Python script located at `/home/user/audit_pipeline.py`. This script is supposed to perform an audit but has a critical flaw and is incomplete.

Your task consists of three phases:

**Phase 1: Fix the SQL Query (Window Functions & Cross Join Bug)**
The script currently executes a SQL query to find the employee with the highest number of sent messages in each department. However, the previous auditor made a mistake: the query contains an implicit cross join that wildly inflates the message counts, and it doesn't correctly isolate the top sender per department.
Modify the SQL query in `/home/user/audit_pipeline.py` so that it:
1. Correctly joins the tables without implicit cross joins.
2. Uses a SQL Window Function (`RANK()` or `ROW_NUMBER()`) to find the exact top sender (by count of messages sent) for each `department`.
3. Outputs the results (Department, Employee ID, Message Count) to `/home/user/top_communicators.csv` (headers: `department,employee_id,message_count`). If there's a tie for first place, include any one of the tied employees.

**Phase 2: Graph Analytics (Centrality)**
The compliance team needs to identify the "hub" of the communication network. 
Extend the Python script to:
1. Query all unique sender-to-receiver pairs from the `communications` table to build a directed graph.
2. Calculate the Betweenness Centrality for all employees in this network. (You may install and use the `networkx` library).
3. Identify the `employee_id` with the highest betweenness centrality.
4. Save this result to `/home/user/highest_centrality.json` in the exact format: `{"employee_id": 12, "centrality": 0.15}` (round centrality to 4 decimal places).

**Phase 3: Graph Traversal (Shortest Path)**
The compliance officer suspects information leaked from Employee ID `3` to Employee ID `18`. 
Extend the script to:
1. Compute the shortest path (unweighted, by number of hops/edges) from Employee ID `3` to Employee ID `18` using the directed graph.
2. Save the path as a list of employee IDs to `/home/user/shortest_path.json` in the exact format: `{"path": [3, 7, 12, 18]}`.

Run your completed pipeline script to generate the three required output files.