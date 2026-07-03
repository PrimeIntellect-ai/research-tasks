You are acting as a technical assistant to a compliance officer auditing an organization's IT infrastructure. We need to identify potential unauthorized access paths to a highly sensitive system called `SYS_OMEGA`.

The infrastructure access data is scattered across three different representations in the `/home/user/compliance_data/` directory:
1. **Relational Data**: `/home/user/compliance_data/employees.csv`
   Format: `employee_id,employee_name,role_id`
2. **Document Data**: `/home/user/compliance_data/roles.json`
   Format: An array of JSON objects mapping roles to the systems they have direct access to.
   Example: `[{"role_id": "R1", "direct_access": ["SYS_A", "SYS_B"]}, ...]`
3. **Graph Data**: `/home/user/compliance_data/network_graph.txt`
   Format: A directed edge list representing network connectivity between systems. Each line contains two space-separated system names: `SOURCE_SYS TARGET_SYS`. This means a user on `SOURCE_SYS` can laterally move to `TARGET_SYS`.

Your task:
1. Map the cross-representation data to trace transitive access paths. An employee can access a system if their role grants direct access, OR if there is a valid directed path through the network graph from any of their directly accessed systems to the target system.
2. Identify all employees who can reach `SYS_OMEGA`.
3. Calculate the *shortest* path length from the employee to `SYS_OMEGA`. (Direct access counts as length 1. Direct access to a system that connects to `SYS_OMEGA` counts as length 2, etc.)
4. Create an output report at `/home/user/audit_report.json`.

The output must exactly match this JSON schema:
A JSON array of objects, sorted first by `shortest_path` (ascending), and then by `employee_name` (alphabetically, ascending).
Each object must have exactly two keys:
- `employee`: (string) The employee's name.
- `shortest_path`: (integer) The minimum path length to SYS_OMEGA.

Example output format:
```json
[
  {
    "employee": "Bob",
    "shortest_path": 2
  },
  {
    "employee": "Alice",
    "shortest_path": 3
  }
]
```

You may use any standard shell tools, `jq`, `sqlite3`, `awk`, or write a script in Python to accomplish this. Ensure your approach handles data mapping efficiently.