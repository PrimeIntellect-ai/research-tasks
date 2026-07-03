You are a data analyst troubleshooting an issue with a company database. 

You have been given an SQLite database at `/home/user/company.db`. Recently, a sudden power failure caused the `idx_sales_date` index on the `sales` table to become corrupted, resulting in queries returning stale or missing rows. 

Your task is to fix the database and create a shell script that generates a top-salesperson report.

Requirements:
1. Repair the corrupted index(es) in `/home/user/company.db`.
2. Write a Bash script at `/home/user/generate_report.sh` that takes a single date argument (in `YYYY-MM-DD` format).
3. The script must query the `company.db` database and output the top 3 employees based on their total sales on or before the provided date.
4. The output must be printed to standard output in CSV format with exactly the following columns:
   `Rank,Employee_Name,Total_Sales,Management_Chain`
5. The `Management_Chain` must be a string representing the hierarchy from the top-level manager (CEO) down to the employee, separated by ` -> ` (e.g., `Alice -> Bob -> Dave`). Use a recursive query to compute this.
6. The `Rank` must be calculated using a window function, ranking by `Total_Sales` descending. If there are ties, order alphabetically by the employee's name.
7. Ensure your script is executable.

Example execution:
`/home/user/generate_report.sh 2023-01-02`

Example output:
```
1,Frank,400,Alice -> Charlie -> Frank
2,Dave,250,Alice -> Bob -> Dave
3,Eve,200,Alice -> Bob -> Eve
```