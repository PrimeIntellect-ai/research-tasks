You are a data analyst tasked with analyzing a company's organizational structure and compensation using a dump of HR data.

You have been provided with a CSV file at `/home/user/employees.csv` containing the following columns:
`emp_id,name,salary,manager_id`

Your goal is to write a Python script at `/home/user/analyze.py` that processes this relational CSV data and performs the following operations:
1. Maps the data into a graph representation where each employee is a node, and the `manager_id` relationship forms an undirected edge (meaning an employee is connected to their manager, and a manager is connected to their direct reports).
2. Computes the shortest path in this organizational graph between the employee with `emp_id` equal to `EMP-012` and the employee with `emp_id` equal to `EMP-007`. 
3. Aggregates the `salary` of all employees that lie on this shortest path (inclusive of both `EMP-012` and `EMP-007`).
4. Outputs the summarized result as a JSON document saved to `/home/user/path_summary.json`.

The output JSON file must have exactly this format:
```json
{
  "path": ["EMP-012", "EMP-...", "EMP-007"],
  "total_salary": 450000
}
```
*(Note: The above values are just examples).*

Ensure your script runs successfully and creates the `/home/user/path_summary.json` file. You can use standard Python libraries.