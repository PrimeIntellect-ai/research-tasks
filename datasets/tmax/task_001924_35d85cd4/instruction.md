You are acting as a Database Administrator for a legacy system where a "NoSQL" document database is actually implemented as a series of massive JSON Lines (JSONL) files. Your predecessor wrote horribly inefficient queries that frequently crash due to memory exhaustion. 

Your task is to build an optimized, parameterized Bash script that functions as a query execution engine and aggregation pipeline using standard Linux shell tools (like `jq`, `grep`, `sort`, `head`, `tail`, `awk`).

**The Data:**
You have a dataset located at `/home/user/data/employees.jsonl`. 
Each line is a JSON object representing an employee, with the following schema:
`{"id": "uuid", "name": "string", "department": "string", "salary": number, "status": "string", "join_date": "YYYY-MM-DD"}`

**The Goal:**
Create a Bash script at `/home/user/query_engine.sh` that accepts command-line parameters to filter, sort, paginate, and project the data. 

**Required Parameters:**
Your script must parse the following arguments (all are optional; handle defaults as specified):
*   `--status <string>` (Filter: exact match for the `status` field. If omitted, do not filter by status)
*   `--min-salary <number>` (Filter: strictly greater than or equal to this salary. Default: 0)
*   `--sort-by <field>` (Sort: field to sort the results by. Default: `id`)
*   `--sort-order <asc|desc>` (Sort: ascending or descending. Default: `asc`)
*   `--skip <number>` (Pagination: number of records to skip. Default: 0)
*   `--limit <number>` (Pagination: max number of records to return. Default: 10)

**Output Specification:**
*   The script must output the final results directly to standard output (STDOUT).
*   The output must be in JSON Lines (JSONL) format (one valid JSON object per line).
*   **Projection:** The output objects must *only* contain the fields: `id`, `name`, `department`, and `salary`. (Drop `status` and `join_date`).
*   **Performance:** Since you are a DBA optimizing this, try to structure your pipeline efficiently (e.g., filter before sorting, use efficient shell pipes where possible).

Make sure the script is executable (`chmod +x`). 
Once your script is ready, you do not need to execute it yourself—an automated test suite will run your script with various parameter combinations to verify its correctness.