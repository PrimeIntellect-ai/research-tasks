You are a Database Reliability Engineer investigating a failing backup pipeline. 

The pipeline's job execution graph is stored in a local SQLite database at `/home/user/backups.db`. Yesterday, a system crash corrupted the primary index (`idx_dep_parent`) on the dependency table, causing standard queries to return stale or cyclic rows and making the backup scheduler crash.

Your task is to write a Python script at `/home/user/solve.py` that does the following:
1. Connects to `/home/user/backups.db`.
2. Bypasses or drops the corrupted index to ensure accurate data retrieval.
3. Reverse engineers the schema to understand how jobs and their dependencies are stored.
4. Uses a Recursive CTE (Common Table Expression) to traverse the job hierarchy and find the shortest execution path (by total job duration) from the job named 'ROOT' to the job named 'LEAF'.
5. Calculates the total duration of this shortest path.
6. Writes the exact sequence of job names and the total duration to `/home/user/solution.txt` in the following exact format: `PATH: ROOT->...->LEAF | DURATION: <total_duration>`

Do not use external Python libraries other than the standard library (e.g., `sqlite3`). Run your script and ensure `/home/user/solution.txt` is created with the correct data.