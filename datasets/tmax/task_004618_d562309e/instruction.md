I need you to process a large hierarchical sales dataset using SQLite, but we are working in an isolated environment. I've provided the source code for SQLite in `/app/sqlite-src-3410200`.

Your goals are to:
1. Fix and compile the vendored SQLite source. The current build configuration has been deliberately crippled to disable crucial analytical features. You must identify the perturbation in the build files, fix it, and compile the `sqlite3` binary within the `/app/sqlite-src-3410200` directory.
2. Write a bash script `/home/user/analyze.sh` that loads `/home/user/sales_data.csv` into a SQLite database (`/home/user/company.db`).
3. Inside your bash script, use the compiled `sqlite3` binary to execute a highly optimized query that generates `/home/user/top_performers.csv`.

**Data Model Reverse Engineering:**
The `/home/user/sales_data.csv` has the following headers: `emp_id`, `manager_id`, `dept_id`, `individual_sales`.
- `emp_id` is the primary key.
- `manager_id` points to the `emp_id` of the employee's manager (null for the CEO).

**Analytical Query Requirements:**
Your query must output a CSV with the following columns: `emp_id`, `dept_id`, `total_team_sales`, `dept_rank`.
- `total_team_sales`: The employee's `individual_sales` PLUS the `individual_sales` of all employees in their entire downline (direct and indirect reports). (Requires recursive/hierarchical CTEs).
- `dept_rank`: The rank of the employee within their department based on `total_team_sales` in descending order. Rank 1 is the highest. (Requires window functions).
- Filter the output to only include employees who rank in the top 3 of their department (`dept_rank` <= 3).
- Order the final result by `dept_id` ascending, then `dept_rank` ascending.

**Performance Constraint:**
Your data schema and query must be extremely efficient. An unoptimized query on this 100,000 row dataset might take >20 seconds. You must implement necessary database optimizations (e.g., indexing) so that the specific query execution time is well under the required metric threshold.

Please ensure `/home/user/analyze.sh` is fully automated, executable, and creates the required database and output CSV file when run. Use bash for the automation wrapper.