I need you to optimize a hierarchical data extraction pipeline. Our current database script tries to map an entire organizational chart by making concurrent recursive calls from application code, which frequently causes SQLite database locks and deadlocks when combined with other system operations. 

To fix this, we need to push the recursion down into the database layer and build a clean pipeline in Rust to extract and serialize the data.

An SQLite database exists at `/home/user/company.db`. It contains a table named `employees` with the following schema:
`id INTEGER PRIMARY KEY, name TEXT NOT NULL, manager_id INTEGER` (where `manager_id` is a foreign key to `employees.id`, and is NULL for the top-level executive).

Please complete the following:
1. Create a new Rust project at `/home/user/org_query`.
2. Write a Rust program that takes exactly one command-line argument: a starting Employee ID.
3. The program must connect to `/home/user/company.db` and execute a single `WITH RECURSIVE` SQL query (CTE) to fetch the target employee and all of their direct and indirect reports (the entire subtree).
4. The query must compute the `depth` of each employee relative to the starting employee. The starting employee has a depth of `0`. Their direct reports have a depth of `1`, and so on.
5. The Rust program must retrieve these records, validate the types, and serialize the result as a JSON array of objects.
6. Each JSON object in the array must strictly match this schema:
   `{"emp_id": <integer>, "emp_name": "<string>", "depth": <integer>}`
7. The JSON array must be sorted by `emp_id` in ascending order.
8. The program must write the final JSON array to `/home/user/reports_output.json`.

You may use crates like `rusqlite`, `serde`, and `serde_json`. Compile the project so that it can be run via `cargo run -- <ID>` inside the `/home/user/org_query` directory.

Once your code is written and compiled, run it with the argument `2` (e.g., `cargo run -- 2`) so that `/home/user/reports_output.json` is generated for my automated verification.