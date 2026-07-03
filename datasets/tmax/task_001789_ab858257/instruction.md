You are tasked with fixing an ETL pipeline issue. We have an SQLite database at `/home/user/etl_data.db` containing an employee hierarchy and their sales records. Due to a recent pipeline failure, the table `sales_raw` contains stale and duplicate rows. 

The table schema is:
`sales_raw (record_id INTEGER, emp_id INTEGER, manager_id INTEGER, sales_amount REAL, updated_at TEXT)`

Your objective is to write a Python script at `/home/user/process_hierarchy.py` that connects to this database, cleans the data, calculates the hierarchical sales aggregates, and exports the results to a structured JSON file.

Specifically, your Python script must execute a SQL query (using window functions and recursive CTEs) that does the following:
1. **Deduplicate:** For each `emp_id`, isolate the single row with the most recent `updated_at` timestamp. Discard the older, stale records.
2. **Hierarchical Aggregation:** Calculate the "total inclusive sales" for every employee. An employee's total inclusive sales is the sum of their own deduplicated `sales_amount` PLUS the deduplicated `sales_amount` of all their direct and indirect subordinates (the entire subtree under them).
3. **Export:** Export the final aggregated data to `/home/user/aggregated_sales.json`.

The output JSON must strictly follow this schema (a list of objects, sorted by `emp_id` in ascending order):
```json
[
  {
    "emp_id": 1,
    "total_inclusive_sales": 1500.50
  },
  ...
]
```

Requirements:
- Ensure the JSON file is properly formatted and conforms exactly to the keys `emp_id` and `total_inclusive_sales`.
- Do not modify the SQLite database itself.
- You must perform the deduplication and hierarchical aggregation inside the SQLite query leveraging standard SQLite features (e.g., `ROW_NUMBER() OVER (...)`, `WITH RECURSIVE`).