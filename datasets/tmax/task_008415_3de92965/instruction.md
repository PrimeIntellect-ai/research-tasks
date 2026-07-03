You are a database administrator tasked with optimizing a highly inefficient process. Currently, developers have a Python script that builds a company's management hierarchy by executing hundreds of individual SELECT queries. This approach is causing severe database contention and occasional transaction deadlocks when run concurrently with HR updates.

Your task is to replace this inefficient traversal with a single optimized query that projects the relational data into a graph-like document format.

You are provided with a SQLite database at `/home/user/corp.db`.
It contains two tables:
1. `employees (emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, dept_id INTEGER)`
2. `departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT)`

Write a Python script at `/home/user/optimize_graph.py` that does the following:
1. Connects to `/home/user/corp.db`.
2. Executes a **single** SQL query using a recursive Common Table Expression (CTE) to retrieve the entire reporting hierarchy starting from the top-level executive (where `manager_id` is NULL).
3. The query must calculate the "depth" of each employee in the hierarchy (the top-level executive is depth 0, their direct reports are depth 1, etc.).
4. The query must join with the `departments` table to retrieve the `dept_name`.
5. The script must export the results to `/home/user/graph_output.json` as a JSON array of objects.

The output JSON must strictly adhere to this schema and be sorted by `emp_id` in ascending order:
```json
[
  {
    "emp_id": 1,
    "name": "Employee Name",
    "manager_id": null,
    "department": "Dept Name",
    "depth": 0
  },
  ...
]
```
Note: If `manager_id` is NULL in the database, it must be `null` in the JSON.
Do not modify the database schema. Only read from it and generate the required JSON file.