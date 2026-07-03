You are acting as a compliance officer auditing our internal systems. We use a custom JSON-based knowledge graph to track user access permissions. The graph contains nodes (Employees, Roles, Systems) and edges (HAS_ROLE, HAS_ACCESS).

We have a script `/home/user/audit.py` that is supposed to identify which employees have access to systems with a `sensitivity` level of `"HIGH"`. Unfortunately, the script was written poorly: it performs an implicit cross-join, ignoring the actual graph edges, and incorrectly flags everyone as having access to everything.

Your task is to fix `/home/user/audit.py` so that it correctly evaluates the knowledge graph pattern:
`(Employee)-[:HAS_ROLE]->(Role)-[:HAS_ACCESS]->(System)`

Requirements:
1. Parse the graph from `/home/user/graph.json`.
2. Find all valid paths where an Employee is connected to a Role via a `HAS_ROLE` edge, and that Role is connected to a System via a `HAS_ACCESS` edge.
3. Filter the paths to only include Systems where `sensitivity` is exactly `"HIGH"`.
4. The output must be a list of dictionaries, each with two keys: `"employee"` (the name of the employee) and `"system"` (the name of the system).
5. Sort the resulting list ascending by employee name, and then ascending by system name.
6. Apply pagination by slicing the sorted list to keep only the first 5 records.
7. Save the final JSON array to `/home/user/audit_results.json`.

Ensure your fixed script runs without errors and produces the correct JSON output.