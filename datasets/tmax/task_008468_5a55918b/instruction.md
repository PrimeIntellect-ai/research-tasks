You are a data engineer tasked with building an optimized ETL pipeline in Bash. You need to process user activity data stored in a SQLite database, optimize the queries, and transform the relational data into a document-oriented JSON representation.

Your system has a SQLite database located at `/home/user/data.db` with two tables:
- `users`: `id INTEGER PRIMARY KEY`, `name TEXT`, `region TEXT`
- `events`: `id INTEGER PRIMARY KEY`, `user_id INTEGER`, `event_type TEXT`, `event_time DATETIME`

There is an `EXPLAIN QUERY PLAN` output saved in `/home/user/plan.txt`. 

Please perform the following steps:

1. **Query Optimization**: Analyze `/home/user/plan.txt`. It indicates a full table scan on one of the tables when joining on `user_id`. You must create an index named `idx_events_user` on the `user_id` column of the `events` table in `/home/user/data.db` to optimize the pipeline.

2. **ETL Script Construction**: Create a Bash script at `/home/user/run_etl.sh` that takes a single argument: a `region` code (e.g., 'NA' or 'EU').
   
   The script must:
   - Accept the region as the first positional parameter (`$1`).
   - Query the `/home/user/data.db` database using parameterized queries (or safe variable substitution in bash for SQLite) to retrieve all users in that region, along with all their associated events.
   - Perform **cross-representation mapping** to transform this relational join into a JSON Lines (JSONL) format. Each line must be a valid JSON object representing one user and their aggregated events, structured exactly like this:
     ```json
     {"user_id": 1, "name": "Alice", "total_events": 3, "event_types": ["login", "click", "logout"]}
     ```
     *(Note: `event_types` should be a JSON array of strings containing all `event_type` values for that user, in the order they appear in the database).*
   - Save the JSONL output to `/home/user/output_<region>.jsonl`.
   - Calculate the user in that region with the highest `total_events`. If there is a tie, pick the one with the lowest `user_id`.
   - Append a summary line to `/home/user/summary.txt` in the exact format: `Region: <region> | Top User: <name> | Events: <count>`.

3. **Execution**: Make sure your script is executable (`chmod +x /home/user/run_etl.sh`). Execute your script once for the region `NA` and once for the region `EU`.

Ensure all files are created exactly at the specified absolute paths.