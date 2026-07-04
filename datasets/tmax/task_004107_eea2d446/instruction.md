You are a database administrator tasked with extracting an organizational reporting metric from a company SQLite database. 

We have an SQLite database located at `/home/user/company.db` with the following schema:
```sql
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT
);

CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    dept_id INTEGER,
    salary INTEGER
);

CREATE TABLE reports_to (
    mgr_id INTEGER,
    emp_id INTEGER,
    PRIMARY KEY (mgr_id, emp_id)
);
```
Recently, an index on `reports_to` was found to be corrupted, but it has been dropped. You need to perform a fresh query.

Your task is to write a Rust program that connects to this database and exports a specific JSON report. 

Create a new Rust project at `/home/user/manager_report`. Modify the project so that when `cargo run` is executed, it calculates the following and writes the output to `/home/user/top_managers.json`:

For each department, find the single employee who has the highest number of direct reports (people who report directly to them in the `reports_to` table). 
- Use a window function to rank the employees within each department.
- If there is a tie in the number of direct reports, break the tie by choosing the employee with the highest `salary`. If there's still a tie, choose the lowest `emp_id`.
- Only include employees who have at least 1 direct report.
- The output must be a JSON array of objects, sorted alphabetically by `dept_name`.

The JSON format must strictly match this structure:
```json
[
  {
    "dept_name": "Engineering",
    "manager_name": "Alice",
    "direct_reports": 5,
    "salary": 120000
  },
  ...
]
```

You may use standard crates like `rusqlite`, `serde`, and `serde_json`. Make sure your Cargo.toml is properly configured and the code successfully compiles and runs.