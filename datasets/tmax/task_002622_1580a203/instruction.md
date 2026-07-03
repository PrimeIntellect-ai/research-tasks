You are acting as an assistant to a compliance officer auditing an organization's IT infrastructure. We need to analyze our access control matrix to find employees who might be over-permissioned. 

I have an SQLite database located at `/home/user/compliance.db` with the following schema:
- `employees` (id INTEGER PRIMARY KEY, name TEXT, department TEXT)
- `resources` (id INTEGER PRIMARY KEY, name TEXT, sensitivity TEXT)
- `access_grants` (emp_id INTEGER, resource_id INTEGER, grant_date TEXT)

Your task has two parts:

1. **Graph Audit Tool (Rust)**
Create a new Cargo project named `access_auditor` in `/home/user/`. Write a Rust program (`src/main.rs`) that connects to `compliance.db` (using the `rusqlite` crate) and performs the following cross-representation graph analysis:
- We want to conceptually treat employees and resources as a bipartite graph.
- Using parameterized queries to prevent SQL injection, query the database for all employees in the "Finance" department.
- For each Finance employee, calculate their "degree centrality" strictly with respect to resources that have a sensitivity level of 'HIGH'.
- Find the single Finance employee with the highest number of 'HIGH' sensitivity access grants.
- Write the result to `/home/user/audit_result.txt` strictly in the format: `EMPLOYEE_NAME:HIGH_SENSITIVITY_COUNT` (e.g., `JohnDoe:4`).
- Compile and run your Rust program to generate this file.

2. **Index Strategy**
Our actual production database has millions of rows, and the queries your Rust program runs would be too slow. 
Create a file named `/home/user/optimize.sql` containing the exact SQL `CREATE INDEX` statements needed to optimize:
- Filtering employees by department.
- Filtering resources by sensitivity.
- Joining the `access_grants` table on both `emp_id` and `resource_id`.

Please complete these steps. I will verify the contents of `/home/user/audit_result.txt` and `/home/user/optimize.sql`.