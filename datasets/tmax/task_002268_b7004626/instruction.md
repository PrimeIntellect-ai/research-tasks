You are acting as a Database Administrator tasked with optimizing and debugging transaction deadlocks. 
We have a system where transactions frequently get stuck in wait states. The wait dependencies are modeled as a directed graph in an SQLite database located at `/home/user/deadlocks.db`.

The database has a single table:
`wait_graph(src_tx TEXT, dst_tx TEXT, wait_time_ms INTEGER)`
Each row indicates that transaction `src_tx` is waiting for transaction `dst_tx`, and has been waiting for `wait_time_ms` milliseconds.

Your task is to write a Python script `/home/user/analyze_deadlocks.py` that finds potential deadlocks represented by dependency cycles of exactly length 3 (i.e., A -> B -> C -> A). 

The script must accept the following command-line arguments:
* `--start-tx` (string): The starting transaction ID (Node A).
* `--min-total-wait` (int): Filter to only include cycles where the sum of `wait_time_ms` across all 3 edges is greater than or equal to this value.
* `--limit` (int): Maximum number of results to return.
* `--offset` (int): Number of results to skip for pagination.

Requirements for the script:
1. It must use the `sqlite3` standard library.
2. It must execute a **single parameterized SQL query** to perform the knowledge graph pattern matching (finding the cycles), filtering, sorting, and pagination. Do not use string formatting (like f-strings) to inject the parameters into the SQL query string; use `?` or named parameters to prevent SQL injection.
3. The query must find paths `A -> B -> C -> A` where `A` is the `--start-tx`.
4. The results must be ordered by the total wait time (sum of the 3 edges) in **DESCENDING** order. If there's a tie, order by node `B`'s ID in **ASCENDING** order, then by node `C`'s ID in **ASCENDING** order.
5. The script must write the final paginated results as a JSON array to `/home/user/deadlock_report.json`.

JSON Output format:
```json
[
  {
    "path": ["TX_A", "TX_B", "TX_C", "TX_A"],
    "total_wait": 1500
  }
]
```

Ensure your script is executable and robust. Do not modify the database.