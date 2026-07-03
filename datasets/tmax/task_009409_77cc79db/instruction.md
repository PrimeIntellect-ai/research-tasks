You are acting as a data analyst. You have been provided with two CSV files in the `/home/user` directory: `employees.csv` and `interactions.csv`.

Your task is to write a Python script at `/home/user/process_data.py` that processes these files to find the top communicators in each department based on their interaction graph.

Here are the requirements for your script:
1. Read `employees.csv` and `interactions.csv`.
2. **Filter and Validate**: Discard any rows in `interactions.csv` where either the `source_id` or `target_id` does not exist in `employees.csv`.
3. **Graph Projection**: Treat the valid interactions as an undirected graph. Calculate the total number of interactions (degree) for each employee. Every valid row in `interactions.csv` adds 1 to the interaction count of its `source_id` and 1 to its `target_id`.
4. **Analytical Aggregation**: For each department, identify the top 2 employees with the highest interaction count. If there is a tie in interaction count, resolve it by sorting by `emp_id` in ascending order. If an employee has 0 valid interactions, they should still be considered (with a count of 0).
5. **Output**: Write the results to `/home/user/top_communicators.json`. The output must be a JSON array of objects, sorted by `department` alphabetically (ascending), then by `interaction_count` descending, and finally by `emp_id` ascending.

Each object in the JSON array must have exactly the following schema:
```json
{
  "department": "String",
  "emp_id": "Integer",
  "name": "String",
  "interaction_count": "Integer"
}
```

Ensure your Python script runs successfully and produces the exact JSON file required. You may use standard libraries and `pandas` if needed.