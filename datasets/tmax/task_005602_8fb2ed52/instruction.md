You are a Data Engineer tasked with reverse-engineering an undocumented legacy ETL scheduling database and extracting data lineage.

You have been given a SQLite database file located at `/home/user/legacy_etl.db`. This database tracks ETL jobs and their dependencies (which jobs must finish before another can start). However, there is no documentation, no foreign keys, and no indexes on the tables. 

Your task involves three phases:

1. **Schema Analysis & Optimization**:
   Inspect `/home/user/legacy_etl.db`. It contains two tables related to jobs and their relationships. 
   Write a Bash script `/home/user/build_indexes.sh` that uses `sqlite3` to add necessary indexes to the database to optimize hierarchical/recursive queries querying for a job's upstream dependencies. Execute this script.

2. **Recursive Lineage Extraction**:
   Write a Bash script `/home/user/get_upstream.sh` that takes a single argument: a `job_name`.
   The script must query the database using a recursive CTE to find ALL upstream dependencies (jobs that must run before the given job, including their dependencies, recursively).
   The script must output a well-formatted JSON array of strings containing the names of all upstream jobs, sorted alphabetically. Do not include the target job itself.
   
   *Example Usage:* `./get_upstream.sh "Aggregate_Weekly"`
   *Example Output:* `["Clean_Data", "Extract_API", "Validate_Format"]`

3. **Execution**:
   Find the upstream lineage for the job named `"Load_Fact_Sales"`.
   Run your script and save the standard output exactly to `/home/user/sales_lineage.json`.

Constraints:
- Use only standard bash tools, `sqlite3`, and `jq` if needed.
- The output JSON must strictly be an array of strings, properly formatted.