You are an ETL data engineer at a tech company. We have a nightly ETL pipeline that extracts relational data from our local SQLite database, converts it into a JSON document format, and then analyzes it as a knowledge graph to find cross-departmental collaborations.

However, the current pipeline is incomplete and terribly slow. 

Here is what you need to do:

1. **Optimize the Relational Query:**
There is a SQLite database located at `/home/user/company.db`. 
You need to add appropriate indexes to the database to optimize query performance for joining `employees`, `departments`, `projects`, and `employee_projects`. 
Then, write a Python script `/home/user/extract.py` using parameterized SQLite queries to extract a list of all employees and their associated projects and departments. 

2. **Cross-Representation Mapping (Relational -> Document):**
The extraction script `/home/user/extract.py` must output the data to `/home/user/graph_data.json` in the following strict document format:
```json
[
  {
    "employee_id": 1,
    "department_id": 101,
    "projects": [201, 202]
  },
  ...
]
```

3. **Knowledge Graph Pattern Matching:**
Write a second Python script `/home/user/analyze.py` that reads `/home/user/graph_data.json`, constructs an undirected graph (using `networkx` or standard dictionaries), and finds all pairs of employees who work in **different** departments but are assigned to the **same** project.
Output these pairs into a CSV file `/home/user/cross_dept_collabs.csv` with the headers: `emp1_id,emp2_id,shared_project_id`.
*Constraint:* Ensure `emp1_id < emp2_id` to avoid duplicates, and sort the final CSV ascending by `emp1_id`, then `emp2_id`, then `shared_project_id`.

Ensure you complete all scripts, run them, and generate the final `cross_dept_collabs.csv` file. You may use `pip install networkx` if you choose to use it.