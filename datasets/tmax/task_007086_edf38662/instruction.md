You are a data engineer building an ETL pipeline to migrate hierarchical relational data into a Neo4j graph database. 

You are provided with an SQLite database at `/home/user/company.db`. It contains a single table `employees` with the following schema:
`employees(emp_id TEXT PRIMARY KEY, name TEXT, manager_id TEXT)`

The `manager_id` references the `emp_id` of the employee's manager. The top-level executive (the CEO) has a `manager_id` of `NULL`.

Your task is to write a Python script named `/home/user/etl_export.py` that performs the following steps:
1. Connects to `/home/user/company.db`.
2. Uses a recursive SQL query (Recursive CTE) to extract all employees along with their "hierarchy level" (the CEO is level 0, their direct reports are level 1, and so on).
3. Exports this data by generating a valid Cypher script named `/home/user/graph_import.cypher`. This script must contain Cypher statements to:
   - Create a node for each employee with the label `Employee` and properties `emp_id` (string), `name` (string), and `level` (integer). Example: `CREATE (:Employee {emp_id: "E1", name: "Alice", level: 0});`
   - Create a `MANAGES` relationship from the manager to the employee for every employee that has a manager. Example: `MATCH (m:Employee {emp_id: "E1"}), (e:Employee {emp_id: "E2"}) CREATE (m)-[:MANAGES]->(e);`
   - Ensure the node creation statements appear before the relationship creation statements, with exactly one statement per line.
4. Generates an index strategy file named `/home/user/index_strategy.cypher` containing exactly two Cypher commands (one per line):
   - A command to create a unique constraint on the `emp_id` property for the `Employee` label.
   - A command to create a standard index on the `level` property for the `Employee` label.

After writing the script, execute it so the output files are generated.