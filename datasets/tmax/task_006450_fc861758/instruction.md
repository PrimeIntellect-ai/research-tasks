You are a database administrator working with a custom Knowledge Graph stored in an SQLite database. 

The database is located at `/home/user/graph.db` and uses a generic edge-list schema to store the graph:
1. `Entity` table: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `label` (TEXT)
2. `Relation` table: `source_id` (INTEGER), `target_id` (INTEGER), `rel_type` (TEXT)

Your task is to write a Python script at `/home/user/query_graph.py` that performs complex graph pattern matching using SQL joins (simulating Cypher/SPARQL semantics) to find a very specific pattern, and then validates the output.

**The Graph Pattern to find:**
Find all instances where:
1. A Person (`A`) `WORKS_FOR` a Department (`B`).
2. That Department (`B`) `MANAGES` a Project (`C`).
3. The Person (`A`) is directly `ASSIGNED_TO` that same Project (`C`).
4. The Person (`A`) `REPORTS_TO` a Manager (`M`, also a Person).
5. The Manager (`M`) `WORKS_FOR` a Department (`D`), but Department `D` is **NOT** the same as Department `B`.

*Node Labels:* Person, Department, Project.
*Relation Types:* WORKS_FOR, MANAGES, ASSIGNED_TO, REPORTS_TO.

**Output Requirements:**
Your Python script must execute this query and format the result as a JSON array of objects.
Each object must have exactly these keys:
- `employee_name` (Name of Person A)
- `department_name` (Name of Department B)
- `project_name` (Name of Project C)
- `manager_name` (Name of Manager M)
- `manager_department` (Name of Department D)

Before saving, your script **must** validate the generated data structure against the JSON schema located at `/home/user/schema.json` using the `jsonschema` Python library. (You can install it if it's not present). 
If validation passes, save the JSON output to `/home/user/output.json`. Sort the JSON array alphabetically by `employee_name` before saving.

Ensure your query is highly optimized, using appropriate table aliases and complex joins. Do not use external graph databases; you must translate the pattern matching into standard SQL for SQLite.