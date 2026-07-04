You are a data analyst processing organizational data. You have been given two flat CSV files representing an organizational knowledge graph:
1. `/home/user/data/nodes.csv` - Contains employee information. Headers: `node_id,name,department`
2. `/home/user/data/edges.csv` - Contains reporting relationships (edges). Headers: `manager_id,employee_id`

Your task is to write a Bash script `/home/user/analyze_graph.sh` that projects this flat data into a queryable graph using `sqlite3`, optimizes the schema, and extracts a specific pattern.

The script must:
1. Accept exactly one argument: a `department` name (e.g., "Engineering").
2. Create an ephemeral SQLite database, import the two CSV files, and construct a parameterized query to find a specific knowledge graph pattern: all instances where a Manager from the target department (argument 1) manages an Employee who is in a *different* department.
3. **Optimize the query**: Create at least one index on the imported tables so that the join/filtering operation does not rely solely on full table scans.
4. Export the `EXPLAIN QUERY PLAN` output of your pattern-matching query to `/home/user/query_plan.txt`. The plan must demonstrate the use of your index(es) (i.e., the word "INDEX" must appear in the plan output for the `nodes` or `edges` table).
5. Output the results of the query to standard output (stdout) in CSV format (without headers). The columns must strictly be: `ManagerName,EmployeeName,EmployeeDept`.

Constraints:
- Use standard bash and `sqlite3`.
- Your script must be executable (`chmod +x`).
- Do not create any permanent databases on disk; you can use in-memory SQLite (`:memory:`) or a temporary file that gets cleaned up.
- Pay attention to CSV headers when importing.

Example expected stdout when running `./analyze_graph.sh "Engineering"`:
```text
Alice,Charlie,Sales
```