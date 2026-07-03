You are a database administrator tasked with optimizing and mapping data queries across different storage representations. Our system stores organizational hierarchy in a relational database and resource permissions in a NoSQL document format. 

Currently, our permission resolution system is slow because it doesn't pre-compute inherited access. We need you to write a Python script that calculates the fully resolved access graph for all employees.

Here is the setup:
1. An SQLite database is located at `/home/user/employees.db`. It contains a table named `org` with the schema `(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)`. The `manager_id` references the `emp_id` of the employee's direct manager. If `manager_id` is null, they are at the top of the hierarchy.
2. A JSON document is located at `/home/user/permissions.json`. It maps `emp_id` (as a string) to a list of `resource_id`s that the employee has been directly granted access to.

**Business Logic for Access:**
An employee has access to:
1. Any resource directly assigned to them in `permissions.json`.
2. Any resource accessible by their direct or indirect reports (i.e., recursive hierarchy).

**Your Task:**
Write and execute a Python script to perform this cross-representation mapping and recursive querying. Generate a single output file at `/home/user/access_graph.json`.

The output file must be a JSON object where the keys are the `emp_id`s (as strings) and the values are lists of `resource_id`s (strings).
- Every employee present in the `org` table must have an entry in the output JSON.
- The list of `resource_id`s for each employee must be **alphabetically sorted** and contain **no duplicates**.
- Ensure your script runs efficiently and successfully writes the file to the exact path specified.