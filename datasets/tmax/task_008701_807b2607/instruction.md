You are a data analyst working with an SQLite database located at `/home/user/company.db`. You've been informed that the database recently suffered from a corrupted index due to a crash, which causes queries joining the `employees` and `departments` tables to return stale or incorrect rows.

Your task is to:
1. Fix the database by rebuilding the corrupted indexes. You must do this using the appropriate SQLite command to rebuild indexes.
2. Reverse engineer the data model of the database to understand the relationship between the `employees` and `departments` tables.
3. Write a Python script at `/home/user/process_salaries.py` that connects to the database, queries the total salary for each department (joining the two tables), and processes the result.
4. Your Python script must validate the query output before exporting: ensure `department_name` is a non-empty string and `total_salary` is an integer. 
5. The script must export the valid data to `/home/user/department_summary.csv` with exactly two columns: `department_name` and `total_salary`, including the header row.
6. Run your Python script to generate the CSV.

Ensure the final CSV file is correctly formatted and contains the accurate aggregated data.