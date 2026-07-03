You are a data analyst working for a retail company. You have been given two CSV files representing the company's organizational hierarchy and individual sales numbers.

The files are located in `/home/user/data/`:
1. `/home/user/data/employees.csv` - Contains columns: `id`, `name`, `manager_id`. (The CEO has an empty string or null for `manager_id`).
2. `/home/user/data/sales.csv` - Contains columns: `id`, `amount`. (Each employee's individual sales for the quarter).

Your task is to write a Python script at `/home/user/hierarchy_sales.py` that processes these CSV files using the `sqlite3` standard library module. The script must compute the **total hierarchy sales** for every employee. An employee's total hierarchy sales is the sum of their own individual sales plus the individual sales of ALL employees who report to them, directly or indirectly (recursive).

The script must fulfill these requirements:
1. Accept exactly two command-line arguments for pagination: `limit` and `offset`. Example: `python /home/user/hierarchy_sales.py 5 0`
2. Ingest the CSV files into an in-memory SQLite database.
3. Use a recursive SQL query (`WITH RECURSIVE`) to calculate the total hierarchy sales for each employee.
4. Filter the results to only include employees whose total hierarchy sales are **greater than or equal to 5000**.
5. Sort the filtered results by `total hierarchy sales` in DESCENDING order. If there is a tie, sort by employee `id` in ASCENDING order.
6. Apply the pagination (`limit` and `offset`) to the final sorted results.
7. Write the paginated output to a CSV file at `/home/user/output.csv` with exactly three columns: `id`, `name`, `total_sales`. Include the header row.

Ensure your script handles standard CSV parsing properly and runs without errors.