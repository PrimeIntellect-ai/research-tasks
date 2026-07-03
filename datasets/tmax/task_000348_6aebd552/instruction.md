You are acting as an AI assistant for a compliance officer auditing an organization's internal network and access controls. 

We have extracted the current IT access configuration into an SQLite database located at `/home/user/audit.db`. 

Your task is to write a Python script `/home/user/audit_path.py` that analyzes this database, projects the relational data into a graph, and finds the shortest potential attack path (or data access path) from a specific employee to a highly sensitive system.

The SQLite database contains the following tables:
1. `employees` (id INTEGER, name TEXT)
2. `systems` (id INTEGER, name TEXT, sensitivity TEXT)
3. `employee_roles` (emp_id INTEGER, role_id INTEGER)
4. `role_access` (role_id INTEGER, system_id INTEGER) - Indicates that a role grants direct access to a system.
5. `system_connections` (source_id INTEGER, target_id INTEGER) - Indicates that a user on the source system can hop to the target system.

**Graph Construction Rules:**
- The graph should be directed.
- Nodes should represent both Employees and Systems. Use their `name` attributes as the node identifiers.
- Add a directed edge from an Employee node to a System node if the employee has a role that grants access to that system (via `employee_roles` joined with `role_access`).
- Add a directed edge from System A to System B if there is a record in `system_connections` where `source_id` is System A and `target_id` is System B.

**The Objective:**
We need to determine if a newly hired intern, "Eve", can indirectly access the "Main_Ledger" system. 
Using your constructed graph, compute the shortest path from "Eve" to "Main_Ledger". 

Your script `/home/user/audit_path.py` must perform this calculation and write the resulting shortest path to a text file located at `/home/user/vulnerability_path.txt`. 
The output in the file must be a single line containing the comma-separated names of the nodes in the path, starting with "Eve" and ending with "Main_Ledger" (e.g., `Eve,Some_System,Another_System,Main_Ledger`). Do not include spaces around the commas or any additional text.

You may install any standard graph libraries like `networkx` to help with the projection and traversal.