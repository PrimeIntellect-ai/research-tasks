You are a data engineer building an ETL pipeline that materializes a knowledge graph from a relational database. 

Our pipeline extracts relationships between employees and the projects they work on, projecting them into a flat edge list (`output_edges.csv`) for a downstream graph database.

Currently, there is a bug in our Rust extraction tool. The tool runs successfully, but the downstream graph database is complaining about millions of duplicate and incorrect edges. It appears the SQL query inside the Rust application has an implicit cross-join (Cartesian product) because it completely skips the associative entity table!

Your task:
1. Navigate to the Rust project at `/home/user/graph_etl`.
2. Inspect and fix the SQL query in `/home/user/graph_etl/src/main.rs`. The query should properly join the `employees` table, the `employee_projects` linking table, and the `projects` table to get the true `(employee_name, project_name)` edges.
3. Optimize the database for this extraction: design a composite index on the `employee_projects` table that would speed up this exact join. Write the exact `CREATE INDEX` SQL statement you would use into a file named `/home/user/index.sql`. Apply this index to the SQLite database (`/home/user/data.db`).
4. Run the fixed Rust project to generate the correct `/home/user/output_edges.csv`.

Database Schema (`/home/user/data.db`):
- `employees` (id INTEGER PRIMARY KEY, name TEXT)
- `projects` (id INTEGER PRIMARY KEY, name TEXT)
- `employee_projects` (emp_id INTEGER, proj_id INTEGER)

Output Requirements:
- `/home/user/output_edges.csv` must contain exactly the valid pairs in the format `employee_name,project_name`.
- `/home/user/index.sql` must contain a valid SQLite `CREATE INDEX` statement on the `employee_projects` table covering both foreign keys.