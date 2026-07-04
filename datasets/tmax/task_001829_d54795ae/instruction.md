You are acting as a data analyst. I have a CSV file located at `/home/user/employees.csv` that contains organizational data. The columns are `emp_id`, `emp_name`, `manager_id`, and `cost`. 

Your task is to write a script in any language of your choice that reads this CSV file, processes the hierarchical relationships (who reports to whom), and computes the total accumulated cost for each employee's team.

You must output a JSON file at `/home/user/org_chart.json` that maps this relational data into a nested document format.

Requirements for the output JSON (`/home/user/org_chart.json`):
1. It must be a valid JSON array of "root" employees (those who have no `manager_id`).
2. The JSON must strictly conform to the JSON Schema provided at `/home/user/schema.json`.
3. Each employee object must have the following keys:
   - `emp_id` (integer)
   - `emp_name` (string)
   - `cost` (integer)
   - `total_team_cost` (integer): The sum of this employee's `cost` and the `total_team_cost` of all their indirect and direct subordinates.
   - `subordinates` (array): A list of nested employee objects who directly report to this employee. If an employee has no subordinates, this must be an empty array `[]`.
4. The `subordinates` array must be sorted by `emp_id` in ascending order.
5. The root array must also be sorted by `emp_id` in ascending order.

Write the code, execute it, and ensure that `/home/user/org_chart.json` is generated correctly and matches the schema requirements.