You are a data engineer building the initial extraction phase of an ETL pipeline. You have been provided with an undocumented SQLite database at `/home/user/supply_chain.db` containing complex logistics network data.

Your objectives are to reverse engineer the data model, extract the optimal routing information, and format the results for the downstream pipeline.

1. **Reverse Engineer the Data Model**: Inspect `/home/user/supply_chain.db`. Identify the tables representing facilities and the transport links between them. Note that some links might be inactive and should not be used.
2. **Pathfinding**: Write a Python script at `/home/user/etl_router.py` to calculate the shortest path (minimizing total cost) strictly over *active* links from the facility named `Alpha_Manufacturing` to `Omega_Distribution`. You may use Python libraries like `networkx` or raw SQL Recursive CTEs.
3. **Query Plan Extraction**: Save the SQLite `EXPLAIN QUERY PLAN` output for the main `SELECT` query you use to extract the link data from the database into a file named `/home/user/query_plan.txt`.
4. **Data Export & Format Conversion**:
   - Run your script to generate a CSV file at `/home/user/optimal_path.csv` with the exact headers: `step_number,location_name,cumulative_cost`. The `step_number` should be 1-indexed (starting at 1 for Alpha_Manufacturing with a cumulative cost of 0).
   - Generate a JSON summary at `/home/user/path_summary.json` with the following schema:
     ```json
     {
       "total_cost": <int>,
       "hop_count": <int>,
       "path": ["Alpha_Manufacturing", "Node_X", ..., "Omega_Distribution"]
     }
     ```

Constraints:
- Only use standard Python 3 libraries or `networkx` (which you can install via pip).
- Ensure all output files are placed exactly at the specified paths in `/home/user/`.