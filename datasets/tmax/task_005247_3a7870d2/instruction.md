You are acting as a data analyst. You have been provided with a CSV file representing an organization's employee hierarchy at `/home/user/employees.csv`. The file contains three columns: `emp_id`, `name`, and `manager_id`. The top-level executive has no `manager_id`.

Your task is to write a Python script at `/home/user/process_hierarchy.py` that reads this CSV and processes it to reverse-engineer the hierarchical data model into a nested document format, similar to what you might use in a NoSQL database.

The script must output a JSON file at `/home/user/hierarchy.json` containing a JSON array of the top-level employees (those with no manager). Each employee object in the JSON must contain the following keys:
- `"emp_id"`: The employee's ID (as a string).
- `"name"`: The employee's name (as a string).
- `"subordinates"`: A recursively nested array of employee objects who directly report to this employee, in the exact same format. If an employee has no subordinates, this should be an empty array `[]`.

The subordinates arrays should be sorted by `emp_id` in ascending order.

Once you have written the script, run it to generate the `/home/user/hierarchy.json` file.