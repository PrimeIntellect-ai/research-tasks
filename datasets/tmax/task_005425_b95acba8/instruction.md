You are a Database Reliability Engineer handling the validation phase of a hybrid database backup system. Your company uses SQLite to track the hierarchical metadata of filesystem backups, and MongoDB to store backup job metrics and telemetry.

You need to write a parameterized Bash script, `/home/user/validate_backup.sh`, that generates the necessary queries to validate a specific tenant's backup on a specific date. 

The script must accept exactly two arguments:
1. `tenant_id` (integer)
2. `backup_date` (string, format YYYY-MM-DD)

Your Bash script must perform the following tasks:

1. **Relational Hierarchical Query**:
   There is an SQLite database located at `/home/user/backup_meta.db`. It contains a table named `filesystem` with the schema:
   `CREATE TABLE filesystem (id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, tenant_id INTEGER);`
   
   Construct and execute a recursive Common Table Expression (CTE) query in SQLite to resolve the full absolute paths of all files/directories belonging to the specified `tenant_id`. 
   * A root directory has `parent_id IS NULL`. 
   * Paths should be formatted with forward slashes (e.g., `root_dir/sub_dir/file.ext`).
   * Output the list of full paths (one per line, sorted alphabetically) to `/home/user/paths.log`.

2. **Query Plan Optimization Analysis**:
   Ensure your recursive query is efficient. Prepend `EXPLAIN QUERY PLAN` to your exact recursive query from step 1, execute it against the SQLite database, and save the raw output to `/home/user/plan.log`. 

3. **NoSQL Aggregation Pipeline Construction**:
   Construct a MongoDB aggregation pipeline that calculates backup sizing metrics for the given tenant and date. Your script must dynamically generate a strict JSON array and save it to `/home/user/mongo_pipeline.json`.
   The pipeline must do exactly the following, in order:
   * Stage 1: Match documents where `tenant_id` matches the script's first argument (as an integer) AND `backup_date` matches the script's second argument (as a string).
   * Stage 2: Group the documents by the field `$region`. In the grouping, calculate a new field named `total_bytes` which is the sum of the `$file_size_bytes` field.

Ensure your script `/home/user/validate_backup.sh` is executable. 

Example invocation:
`/home/user/validate_backup.sh 455 2023-11-20`