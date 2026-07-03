You are a data analyst working on analyzing internal company communication networks. You have been given two CSV files representing a relational dataset of employee interactions. Your goal is to map this relational data into a graph representation, compute a graph analytics metric, perform an aggregation similar to a NoSQL aggregation pipeline, and export the results to a specific JSON document format.

You must write a Rust program to perform this data processing task. You can use standard Rust tooling (`cargo`) to create the project in `/home/user/network_analyzer`.

Here are the input files you will find in `/home/user/`:

1. `users.csv` (Schema: `user_id,department,name`)
2. `interactions.csv` (Schema: `source_id,target_id`) - Represents a directed interaction from `source_id` to `target_id`.

Your Rust application needs to perform the following steps:
1. Parse both CSV files.
2. Build a directed graph from `interactions.csv` and compute the **In-Degree Centrality** for each user. For this task, the in-degree centrality is simply the absolute count of incoming interactions (edges) to a given `target_id`.
3. Map these centrality scores back to the users and their respective departments (cross-representation mapping). If a user has no incoming interactions, their in-degree is 0.
4. Perform a data aggregation (simulating a NoSQL `$group` pipeline stage): Group the users by `department` and calculate the sum of the in-degree centralities of all users within each department.
5. Export the aggregated query results into a JSON array file located exactly at `/home/user/department_influence.json`.

The output JSON file must have exactly the following structure and be sorted alphabetically by the `department` name:
```json
[
  {
    "department": "DepartmentName1",
    "total_in_degree": 10
  },
  {
    "department": "DepartmentName2",
    "total_in_degree": 5
  }
]
```
Ensure your Rust program runs successfully and generates the correct `/home/user/department_influence.json` file. Use whitespace formatting in your JSON exactly as shown (2-space indentation).