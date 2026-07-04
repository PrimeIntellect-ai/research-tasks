You are a data engineer tasked with building an ETL pipeline to migrate organizational data from a NoSQL JSONL format into a relational database, and then performing a hierarchical aggregation.

Your environment contains a raw NoSQL data dump located at `/home/user/raw_org.jsonl`. Each line is a JSON object representing an employee, their salary, and their manager. 

Your task is to write a Rust program that completes the following pipeline:
1. Create a new Rust project at `/home/user/etl_job`.
2. Parse the `/home/user/raw_org.jsonl` file.
3. Create a SQLite database at `/home/user/org.db` with a table named `employees` having the schema:
   `emp_id TEXT PRIMARY KEY, name TEXT, manager_id TEXT, salary INTEGER`
4. Load the parsed data into this SQLite database. 
5. Write a SQL query using a **Recursive CTE** that calculates the total organizational salary budget for *every* employee. An employee's total budget is their own salary plus the salaries of all their direct and indirect subordinates (the entire tree under them).
6. Execute this query in your Rust program and write the results to a CSV file at `/home/user/hierarchy_budgets.csv`. The CSV must have exactly two columns: `emp_id` and `total_budget`, sorted by `total_budget` descending, then by `emp_id` ascending. Do not include a header row.
7. Save the exact SQL query string you used for the Recursive CTE into `/home/user/recursive.sql`.
8. Execute an `EXPLAIN QUERY PLAN` on your recursive CTE and save the raw output lines into `/home/user/plan.txt`.

Ensure your Rust program can be run with `cargo run --manifest-path /home/user/etl_job/Cargo.toml`. You may use crates like `rusqlite`, `serde`, and `serde_json`.