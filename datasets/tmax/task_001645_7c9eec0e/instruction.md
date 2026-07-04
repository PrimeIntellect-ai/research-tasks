You are a database administrator tasked with optimizing and extracting analytics from an SQLite database containing a hierarchical task execution graph.

The database is located at `/home/user/dag.db`. It contains a table `tasks` with the following schema:
- `id INTEGER PRIMARY KEY`
- `parent_id INTEGER` (references `id` of the parent task; `NULL` for the root task)
- `duration INTEGER` (execution time of the task)

**Issues to Resolve:**
1. **Corrupted Index:** The database currently contains a corrupted index named `idx_parent` which is causing stale rows to be returned or full table scans to occur. You must drop this index and recreate it properly on the `parent_id` column.
2. **Critical Path Calculation:** You need to find the critical path of the execution graph. The critical path is defined as the maximum total duration accumulated from the root task (`id = 1`) down to any leaf task (a task with no children).

**Your Objectives:**
Write a Bash script at `/home/user/analyze_graph.sh` that performs the following steps when executed:
1. Fixes the index issue in the SQLite database by dropping `idx_parent` and creating a new index named `idx_parent_id` on the `parent_id` column.
2. Executes a Recursive CTE query against `/home/user/dag.db` to calculate the total duration of all paths from the root to the leaves.
3. Processes the query results using Bash tools (e.g., `awk`, `sort`, `head`, or within SQLite itself) to find the absolute maximum path duration.
4. Writes the final maximum duration to `/home/user/critical_path.txt` in the exact format: `Critical Path Length: <MAX_DURATION>`
5. Generates the `EXPLAIN QUERY PLAN` output for your recursive CTE query and saves it directly to `/home/user/plan.txt`.

**Constraints:**
- The script must be written in Bash and be executable (`chmod +x /home/user/analyze_graph.sh`).
- Do not use Python, Perl, or Ruby; rely on Bash and the `sqlite3` command-line interface.
- Ensure your CTE correctly sums the `duration` values hierarchically.