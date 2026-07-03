You are a data engineer working on migrating and aggregating a legacy HR/Sales database into a modern NoSQL document store. 

We have a proprietary legacy data extraction tool located at `/app/fetch_sales_graph`. This tool is a compiled binary. When executed without arguments, it dumps the entire corporate sales hierarchy to `stdout` in a flat, pipe-separated relational format:
`employee_id|manager_id|direct_sales_amount`
(Note: The top-level CEO has no `manager_id`, represented as an empty string or NULL equivalent depending on how you parse it).

Your objective is to build an ETL pipeline in Bash that maps this flat relational data into a hierarchical graph, calculates recursive aggregations, and outputs a NoSQL-friendly JSON format.

Write a Bash script at `/home/user/etl.sh` that does the following:
1. Executes `/app/fetch_sales_graph` to retrieve the raw data.
2. Ingests the data into an in-memory or temporary datastore (e.g., using `sqlite3`).
3. Uses recursive queries (e.g., Recursive CTEs) to compute the **total rollup sales** for *every* employee in the company. An employee's total rollup sales is defined as their own `direct_sales_amount` PLUS the `direct_sales_amount` of all employees reporting to them, directly or indirectly, all the way down the tree.
4. Outputs the final aggregated data to `stdout` as a JSON array of objects, formatted strictly like this:
```json
[
  {
    "employee_id": "E001",
    "total_rollup_sales": 15000.50
  },
  ...
]
```

Requirements:
- The output must be valid JSON.
- The output should contain an entry for every employee.
- Make sure `/home/user/etl.sh` has executable permissions.
- You may use standard Linux utilities (`awk`, `jq`, `sqlite3`, etc.).

An automated evaluation script will run your `etl.sh` and compare its output against a mathematically perfect rollup of the underlying graph data. The system will calculate an exact match accuracy metric for all employee records.