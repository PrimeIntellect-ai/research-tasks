You are a data engineer tasked with building an ETL pipeline script to extract and summarize hierarchical data from a legacy database. 

You have been provided with an SQLite database file at `/home/user/legacy_system.db`. The database contains three tables with no explicit foreign key constraints and somewhat generic column names. The tables contain employee records, department mappings, and individual sales transactions.

Your task is to:
1. Reverse engineer the data model to understand how the three tables relate to one another (employees, departments, and transactions). Identify the implicit hierarchical reporting structure among employees.
2. Write a Bash script located at `/home/user/generate_report.sh` that queries the database and computes the "Total Team Sales" for every employee.
    * An employee's "Total Team Sales" is defined as their own personal sales plus the total personal sales of all employees who report to them, directly or indirectly (a recursive hierarchy).
    * Employees with no sales should be treated as having 0 personal sales.
3. Your bash script must output a strictly formatted CSV file to `/home/user/team_sales_report.csv`.
    * The CSV must have the following header: `Employee Name,Department Name,Personal Sales,Total Team Sales`
    * The rows must be sorted by `Total Team Sales` in descending order. If there is a tie, sort by `Employee Name` in ascending alphabetical order.
    * All numeric values should be integers. 

Requirements:
- Ensure your script `/home/user/generate_report.sh` is executable.
- Do not install any external tools; use standard Linux utilities and `sqlite3`.
- The output CSV must match the expected format exactly.