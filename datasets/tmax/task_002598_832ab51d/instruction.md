You are a data engineer building an ETL pipeline configuration generator. We have a metadata repository stored as a SQLite database that defines a directed acyclic graph (DAG) of ETL jobs and their dependencies. 

The database is located at `/home/user/etl_metadata.db`.
It has two tables:
1. `jobs`: Contains `id` (INTEGER PRIMARY KEY), `name` (TEXT), and `base_cost` (INTEGER). `base_cost` represents the execution time/cost of that individual job.
2. `dependencies`: Contains `parent_id` (INTEGER) and `child_id` (INTEGER). Both are foreign keys to `jobs.id`.

Your task is to write a Python script that calculates the maximum cumulative execution cost to reach each "leaf" job starting from a specific root job named `'extract_sales_data'`. 

A "leaf" job is defined as a job that has no children (no entries in `dependencies` where it is the `parent_id`).
The cumulative execution cost of a path is the sum of the `base_cost` of all jobs in that path, inclusive of the root and leaf nodes. Because there can be multiple paths to the same leaf job, you must find the *maximum* possible path cost for each leaf.

Write a Python script (you can name it whatever you like, e.g. `solve.py`) to perform this query, ideally leveraging a Recursive CTE (Common Table Expression) to traverse the graph. 

The script must output a JSON file at `/home/user/pipeline_plan.json`. 
The JSON should be an array of objects, sorted by `total_path_cost` in descending order.

Example format for `/home/user/pipeline_plan.json`:
```json
[
  {
    "leaf_job": "some_leaf_job_name",
    "total_path_cost": 250
  },
  {
    "leaf_job": "another_leaf",
    "total_path_cost": 180
  }
]
```

Ensure the output file has exactly this structure and keys.