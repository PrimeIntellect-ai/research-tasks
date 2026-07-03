You are a data analyst tasked with processing an employee organizational hierarchy. 

You have been provided with a CSV file at `/home/user/employees.csv` containing the following columns: `emp_id`, `name`, `manager_id`, and `salary`. The `manager_id` column represents the `emp_id` of the employee's direct manager. The CEO has an empty `manager_id`.

Your task is to write a Python script `/home/user/org_query.py` that computes the total size and combined salary of any sub-organization within the company. 

Requirements for `/home/user/org_query.py`:
1. It must accept a single command-line argument: the `emp_id` of the target manager.
2. It must load the data from `/home/user/employees.csv` into a SQLite database (in-memory is fine).
3. It must use a parameterized SQL query featuring a **recursive CTE** to find the manager and all of their direct and indirect subordinates.
4. It must compute the total number of employees in this hierarchy (including the manager) and their total combined salary.
5. It must output the results as a strictly validated JSON file to `/home/user/output.json` with the following schema:
   - `manager_id`: (integer) The ID passed as an argument.
   - `total_employees`: (integer) The count of employees in the sub-organization.
   - `total_salary`: (integer) The sum of salaries for the sub-organization.

Do not print anything to standard output. Only create the required JSON file. Ensure your script correctly handles parameterized inputs to prevent SQL injection, even when querying in-memory data.