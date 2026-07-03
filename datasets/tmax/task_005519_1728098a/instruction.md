As a compliance officer, you are conducting a system audit to verify which employees have access to sensitive internal systems. The access control data is stored in a relational SQLite database, but your auditing tools require a graph representation in JSON format. Furthermore, the database is currently unoptimized and queries are running too slowly.

Your task has two parts:

1. **Database Optimization (Index Strategy):**
   The database is located at `/home/user/audit.db`. 
   It contains three tables:
   - `employees (id INTEGER PRIMARY KEY, name TEXT)`
   - `group_members (emp_id INTEGER, group_id INTEGER)`
   - `group_access (group_id INTEGER, system_id INTEGER, system_name TEXT)`

   Currently, finding an employee's access requires a full table scan across the mapping tables. Interpret the implicit query plan for joining these tables from `employees` to `group_access`, and design an index strategy. 
   Create exactly two indexes in the database to optimize this join path:
   - Name one index `idx_gm_emp` on the appropriate column in `group_members`.
   - Name the second index `idx_ga_group` on the appropriate column in `group_access`.

2. **Graph Projection & Cross-Representation (Bash Script):**
   Write a Bash script at `/home/user/generate_graph.sh` that queries the SQLite database and materializes the relational data into a Graph Document (JSON).
   
   The script must execute the optimized queries and output a JSON file to `/home/user/audit_graph.json` with the following strict structure:
   ```json
   {
     "nodes": [
       {"id": "emp_<id>", "type": "employee", "name": "<employee_name>"},
       {"id": "sys_<id>", "type": "system", "name": "<system_name>"}
     ],
     "edges": [
       {"source": "emp_<id>", "target": "sys_<id>", "relation": "HAS_ACCESS"}
     ]
   }
   ```
   *Requirements for the JSON:*
   - All employees must be listed as nodes, even if they have no access.
   - All systems present in `group_access` must be listed as nodes.
   - Node arrays and Edge arrays should contain unique entries (no duplicate nodes or edges, even if an employee is in multiple groups granting access to the same system).
   - Do not include 'group' nodes. Project the graph directly from employee to system.
   
Ensure your Bash script is executable and performs the extraction and formatting automatically when run without arguments. Do not use external services or databases; rely on `sqlite3`, standard Linux text utilities (like `jq`, `awk`), or inline scripts within the Bash file.