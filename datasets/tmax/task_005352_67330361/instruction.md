You are a data engineer building an ETL pipeline to process a company's organizational graph. You have been given a raw CSV file representing an employee hierarchy (a directed graph of manager-to-employee relationships) and you need to build a C++ tool to traverse, filter, and format this data.

The raw data is located at `/home/user/org_data.csv` and has the following header and format:
`emp_id,mgr_id,name,salary`
(Note: The top-level executive has a `mgr_id` of `NULL`).

Your task:
1. Write a C++ program at `/home/user/graph_etl.cpp` that reads the CSV and builds an in-memory graph.
2. The program must accept the following command-line arguments:
   `--manager-id <ID>`: The root employee ID to start the recursive search.
   `--min-salary <INT>`: The minimum salary threshold (inclusive).
   `--limit <INT>`: The maximum number of results to return.
   `--offset <INT>`: The number of results to skip.
   `--output <FILE>`: The path where the JSON result should be saved.
3. The program must perform a recursive/hierarchical graph traversal to find ALL direct and indirect reports under the given `--manager-id` (excluding the manager themselves).
4. Filter the found reports to keep only those with `salary >= min-salary`.
5. Sort the filtered reports by `salary` in descending order. If there is a tie, sort by `emp_id` in ascending order.
6. Apply the pagination constraints (`--offset` then `--limit`) to the sorted results.
7. Export the final results to the `--output` file as a properly formatted JSON array of objects. Each object must have exactly three keys: `emp_id` (integer), `name` (string), and `salary` (integer). Example JSON structure:
```json
[
  {"emp_id": 10, "name": "Judy", "salary": 115000},
  {"emp_id": 5, "name": "Eve", "salary": 110000}
]
```
8. Finally, write a bash script at `/home/user/run_pipeline.sh` that:
   - Compiles `graph_etl.cpp` into an executable named `graph_etl` using `g++` (C++17 standard).
   - Runs the executable to find the direct and indirect reports of manager `1`, with a minimum salary of `100000`, a limit of `3`, an offset of `2`, outputting to `/home/user/reports.json`.
   - Uses `jq` to parse `/home/user/reports.json` and extracts just the `name` field of each array element, writing them line-by-line to `/home/user/final_report.txt`.

Ensure your bash script has executable permissions (`chmod +x`). 
Run your bash script to produce the final `final_report.txt`.