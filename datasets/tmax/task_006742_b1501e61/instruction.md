You are a Database Administrator working on a manufacturing system. We have a daily export of our Bill of Materials (BOM) in a CSV file, but the queries running against it are too slow and the output needs to be formatted for a downstream dashboard.

A raw dataset is located at `/home/user/raw_parts.csv` with the following columns (no header):
`id`, `parent_id`, `name`, `cost`

(Note: `parent_id` is empty for root assemblies).

Your task is to write a Bash script `/home/user/process_bom.sh` that does the following:

1. **Database Setup**: Initialize an SQLite database at `/home/user/bom.db` with a table named `parts` (`id INTEGER PRIMARY KEY`, `parent_id INTEGER`, `name TEXT`, `cost REAL`). Import the data from `/home/user/raw_parts.csv` into this table.
2. **Index Optimization**: The downstream query will recursively join on `parent_id`. Create an appropriate index in the database to optimize this lookup.
3. **Recursive and Analytical Query**: Write an SQL query that:
   - Uses a recursive CTE to calculate the `depth` of each part in the assembly tree (root nodes where `parent_id IS NULL` have depth 0, their children depth 1, etc.).
   - Uses a Window Function to calculate `cost_rank`: the rank of the part's cost within its specific `depth` level (highest cost gets rank 1. In case of a tie, order by `id` ascending).
   - Filters the result to only return parts where `cost_rank` is 1 or 2.
   - Selects `id`, `name`, `depth`, `cost`, and `cost_rank`.
   - Orders the final output by `depth` ascending, then `cost_rank` ascending.
4. **Execution Plan**: Before executing the query, run an `EXPLAIN QUERY PLAN` for it and save the exact output to `/home/user/query_plan.txt`.
5. **Export Result**: Execute the query and export the results to a JSON file at `/home/user/top_parts.json`. The JSON should be an array of objects, with keys exactly matching the selected columns (`id`, `name`, `depth`, `cost`, `cost_rank`).

Requirements:
- Ensure your Bash script `/home/user/process_bom.sh` is executable and can be run without any arguments.
- Use `sqlite3` command-line tool within your bash script.
- Ensure the index you create is actually used in the query plan (the plan in `/home/user/query_plan.txt` should mention your index).