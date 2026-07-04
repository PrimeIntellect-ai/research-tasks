You are acting as a compliance officer auditing an internal access control system. 

You have been provided with an SQLite database at `/home/user/compliance.db`. It contains relational access logs and a graph-based representation of network permissions.

The database has the following schema:
1. `employees` table:
   - `emp_id` (TEXT)
   - `assigned_node` (TEXT) - The starting network node assigned to the employee.
2. `network_edges` table:
   - `source` (TEXT)
   - `target` (TEXT)
   - Represents directed connections between network nodes.
3. `access_logs` table:
   - `log_id` (INTEGER)
   - `emp_id` (TEXT)
   - `accessed_node` (TEXT)
   - `timestamp` (TEXT)

**Compliance Rule:**
An employee is only permitted to access a network node if it is reachable from their `assigned_node` within **2 or fewer directed hops** (i.e., path length $\le$ 2) in the `network_edges` graph. A node is always reachable from itself (path length 0).

Your task is to write a Python script at `/home/user/audit.py` that:
1. Connects to `/home/user/compliance.db`.
2. Materializes the graph from `network_edges` in memory.
3. For each employee, calculates the set of legally accessible nodes.
4. Scans the `access_logs` table (using parameterized query construction) to find any access events that violate the compliance rule.
5. Writes all unique violations to `/home/user/violations.csv`.

**Output Format:**
The output file `/home/user/violations.csv` must be a CSV file with the following headers: `emp_id,accessed_node`.
The rows should be sorted alphabetically by `emp_id`, and then by `accessed_node`.
Do not include duplicate violations (if an employee illegaly accessed the same node multiple times, only list it once).

Run your script to generate the `/home/user/violations.csv` file.