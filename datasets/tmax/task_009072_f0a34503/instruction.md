You are a data engineer debugging an ETL pipeline. A previous engineer wrote a Python script (`/home/user/etl_pipeline.py`) that extracts transaction data from a SQLite database (`/home/user/data.db`) and exports an edge list for network analysis. 

However, there are two major problems:
1. The SQL query inside the script returns millions of incorrect rows due to an implicit cross join.
2. The pipeline is missing a required analytical calculation.

Your task is to:
1. **Fix the implicit cross join** in `/home/user/etl_pipeline.py` so that it correctly joins the `users` and `transactions` tables. A transaction should accurately link a sender to a receiver.
2. **Add a window function** to the SQL query to compute a new column called `cumulative_sent`. This column should represent the running total of `amount` sent by the `sender`, ordered by `timestamp` (ascending).
3. **Execute the corrected pipeline** so it generates the expected `/home/user/edges.csv` file containing the columns: `sender`, `receiver`, `amount`, `timestamp`, and `cumulative_sent`.
4. **Compute the shortest path** using the corrected `edges.csv`. Write a new script to perform a directed graph traversal to find the shortest path (minimum number of hops) from `user_1` to `user_9`. 
5. **Export the final results** to `/home/user/final_output.json`. The JSON must exactly match this structure:

```json
{
  "shortest_path": ["user_1", "...", "user_9"],
  "user_9_max_cumulative_sent": <float>
}
```

*Note on `user_9_max_cumulative_sent`: This should be the maximum `cumulative_sent` value where `user_9` was the sender across all their transactions. If they never sent anything, use `0.0`.*

Constraints:
- Do not use external graph libraries like `networkx`; implement the shortest path algorithm (e.g., BFS) using standard Python.
- Both scripts must be run within the `/home/user` directory.