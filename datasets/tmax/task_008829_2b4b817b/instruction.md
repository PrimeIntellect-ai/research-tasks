You are helping a researcher organize and analyze a complex dataset of research artifacts. The relationships between these artifacts are stored in a SQLite database located at `/home/user/research_data.db`. 

The database contains two tables:
1. `artifacts` (`id` INTEGER PRIMARY KEY, `name` TEXT)
2. `relationships` (`source_id` INTEGER, `target_id` INTEGER)

The researcher wrote a Python script at `/home/user/find_path.py` that uses a recursive Common Table Expression (CTE) in SQLite to find the shortest path length between the artifact named 'Alpha' and the artifact named 'Omega'. However, the script is currently hanging and returns incorrect results because the recursive CTE contains a logical error (an implicit cross join or missing join condition) that causes an infinite loop and an explosion of rows. Furthermore, the `relationships` table lacks any indexes, making querying very slow.

Your task is to:
1. Debug and fix the SQL query in `/home/user/find_path.py` so that it correctly computes the shortest path length (number of edges) from 'Alpha' to 'Omega'. The script should write the integer value of the shortest path length to `/home/user/result.txt`.
2. Design and create the necessary index(es) on the `relationships` table to optimize this graph traversal. 
3. Save the exact `CREATE INDEX` statement(s) you executed into `/home/user/indexes.sql`.
4. Run your fixed script so that `/home/user/result.txt` is produced.

Constraints:
- Do not change the output format of `/home/user/result.txt` (it should just be a single integer).
- You may rewrite the Python script to use a different traversal method (like a BFS in Python) if you prefer, as long as it correctly finds the shortest path length and runs efficiently.
- Ensure your index strategy makes traversing from `source_id` to `target_id` efficient.