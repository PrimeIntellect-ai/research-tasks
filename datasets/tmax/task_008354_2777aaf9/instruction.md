You are a data analyst working with employee hierarchy data. You have been given a CSV file at `/home/user/org_chart.csv` containing the company's organizational structure. 

The CSV has the following columns:
`id`, `name`, `manager_id`
(The CEO has an empty `manager_id`)

Your task is to write and execute scripts (using Python, Bash, or SQLite commands) to perform the following end-to-end data processing workflow:

1. **Database Initialization & Import:** Create a SQLite database at `/home/user/org.db`. Create a table named `employees` and load the data from `org_chart.csv` into it. Ensure `id` and `manager_id` are treated as integers, and the CEO's `manager_id` is parsed as `NULL`.
2. **Index Optimization:** Create an index named `idx_manager` on the `manager_id` column to optimize hierarchical queries.
3. **Recursive Querying:** Write a Recursive Common Table Expression (CTE) to calculate the full management path from the CEO (root) down to every employee. The path should be formatted as a string of IDs joined by `->` (e.g., `"1->2->5->8"`).
4. **Data Export & Format Conversion:** Filter the query results to only include employees who are deeply nested in the organization—specifically, employees whose hierarchy path contains 4 or more nodes (including the CEO). Export these filtered results to a JSON file at `/home/user/deep_org.json`.

The output file `/home/user/deep_org.json` must contain a JSON array of objects, sorted by `id` in ascending order. Each object must have exactly two keys: `"id"` (integer) and `"path"` (string).

Example of expected JSON format:
```json
[
  {
    "id": 14,
    "path": "1->3->6->14"
  },
  ...
]
```

Complete this task by executing the necessary commands in the terminal.