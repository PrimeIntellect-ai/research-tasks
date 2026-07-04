You are a database administrator. A junior developer wrote a Bash script (`/home/user/report.sh`) to generate a sales leaderboard from a SQLite database (`/home/user/company.db`). However, the script is running extremely slowly and outputting highly inflated numbers because the SQL query contains an implicit cross join. 

Your task is to fix the SQL query, add analytical window functions, implement parameterized pagination and filtering in the Bash script, and export the results cleanly.

Here is the schema of `/home/user/company.db`:
- `departments` (id INTEGER PRIMARY KEY, name TEXT)
- `employees` (id INTEGER PRIMARY KEY, dept_id INTEGER, name TEXT)
- `sales` (id INTEGER PRIMARY KEY, emp_id INTEGER, amount REAL)

Requirements for the updated `/home/user/report.sh`:
1. **Fix the Query**: Correct the joins so `employees`, `departments`, and `sales` are linked by their foreign keys (`dept_id` and `emp_id`). Only include employees who have at least one sale.
2. **Analytical Aggregation**: Calculate the total sales (`TotalSales`) for each employee. Add a window function to calculate `DeptRank`: the employee's rank within their department based on `TotalSales` (highest sales gets rank 1).
3. **Parameterization & Pagination**: The script must accept exactly 4 arguments:
   - `$1`: `DEPT_FILTER` - Either a specific department ID (e.g., `2`) or the exact string `ALL`. If `ALL`, include all departments.
   - `$2`: `LIMIT` - The maximum number of rows to return.
   - `$3`: `OFFSET` - The pagination offset.
   - `$4`: `OUTPUT_FILE` - The absolute path where the results should be saved.
4. **Result Export**: Execute the query against `/home/user/company.db` and output the results to `$OUTPUT_FILE` as a CSV file (comma-separated).
   - The CSV must include a header row exactly as: `Employee,Department,TotalSales,DeptRank`
   - Order the final output by `Department` name ASC, then `DeptRank` ASC, then `Employee` name ASC.
5. **Bash-centric**: You must write this logic entirely within `/home/user/report.sh`, using the `sqlite3` CLI tool.

Make sure the script is executable (`chmod +x /home/user/report.sh`).