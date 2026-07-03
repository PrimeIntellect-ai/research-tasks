You are a data analyst tasked with processing an organization's communication network using Python. You have been provided with two CSV files:

1. `/home/user/nodes.csv`: Contains employee metadata with columns `id` (integer), `name` (string), and `dept` (string).
2. `/home/user/edges.csv`: Contains communication logs with columns `source` (integer, employee ID), `target` (integer, employee ID), and `weight` (integer, message length).

Your objective is to write a Python script at `/home/user/analyze.py` that performs the following steps:
1. Creates a local SQLite database at `/home/user/network.db`.
2. Reads the CSV files and inserts their data into two tables (`nodes` and `edges`) using strictly **parameterized queries** for the insertions.
3. Uses a **SQL Window Function** to calculate the rank of employees within their department based on their total outgoing message weight (sum of `weight` where they are the `source`).
4. Uses **SQL self-joins (Graph Pattern Matching)** to find all directed triangles in the network. A directed triangle exists if there is a path `A -> B -> C -> A`. 
5. Outputs the results to a JSON file at `/home/user/report.json` with the following exact structure:
```json
{
  "top_per_dept": {
    "DeptName1": <id_of_top_employee_in_dept1>,
    "DeptName2": <id_of_top_employee_in_dept2>
  },
  "triangles": [
    [<node1>, <node2>, <node3>]
  ]
}
```
*Note for `triangles`: Each triangle should be represented as a list of its 3 constituent node IDs sorted in ascending order. The list of triangles should also be uniquely distinct (do not list the same triangle multiple times).*
*Note for `top_per_dept`: If there's a tie, choose the employee with the smaller `id`.*

Run your Python script to generate the database and the `report.json` file.