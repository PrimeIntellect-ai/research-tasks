You are a data engineer building an ETL pipeline to analyze organizational hierarchies. 

We have a SQLite database located at `/home/user/company.db`. It contains a single table representing an adjacency list of an employee hierarchy:
`employees (emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)`

The CEO has a `manager_id` of `NULL` and is at depth 0. Employees reporting directly to the CEO are at depth 1, and so on.

Your task is to:
1. Write a Python script at `/home/user/graph_etl.py` that accepts a single integer command-line argument representing a target hierarchy `depth`.
2. The script must connect to `/home/user/company.db` and use a **recursive CTE (Hierarchical Query)** to traverse the tree and calculate the depth of every employee.
3. Using parameterized query execution, filter the results to only include employees exactly at the target `depth`.
4. Materialize the result by writing a JSON file to `/home/user/output_depth_<depth>.json`. 

The output JSON file must have exactly this format:
```json
{
  "target_depth": 2,
  "employees": [
    "Alice",
    "Bob",
    "Charlie"
  ]
}
```
*Note: The `employees` list must be sorted alphabetically by name.*

Once your script is ready, run it to generate the report for depth `2`.
Make sure the final output file `/home/user/output_depth_2.json` is successfully created.