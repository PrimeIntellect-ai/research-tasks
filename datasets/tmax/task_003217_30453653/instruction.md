You are a Database Reliability Engineer (DBRE) responsible for the backup infrastructure. We track our database backups, their sizes, and how they replicate across different storage nodes in a local SQLite database located at `/home/user/backup_metadata.db`.

Recently, our automated reporting script (`/home/user/generate_report.py`) started producing wildly incorrect total backup sizes. We suspect there is an implicit cross join in the SQL query calculating the analytical aggregations. 

Furthermore, we need to enhance this script to trace the replication path of backups. Our backups land on an initial storage node and are then replicated across a network of nodes until they reach a node in the 'archive' region. This network is stored as a graph in the `replication_links` table.

Your task is to fix and enhance `/home/user/generate_report.py`:
1. **Fix the Analytical Query:** Identify and fix the implicit cross join in the existing query so that the `total_backup_size` per database calculates correctly using window functions.
2. **Graph Traversal:** Add a new query using a Recursive Common Table Expression (CTE) to find the *shortest path* (fewest number of hops) from the initial storage node of the latest backup job to any storage node located in the 'archive' region.
3. **Parameterized Construction:** The script must accept a database name as a command-line argument (e.g., `python3 /home/user/generate_report.py "prod-db-1"`). Use parameterized queries to prevent SQL injection.
4. **Output:** The script must write the result for the requested database to a JSON file at `/home/user/report.json` in the exact following format:
```json
{
  "database_name": "prod-db-1",
  "correct_total_backup_size": 10500,
  "shortest_archive_path": ["node_A", "node_C", "node_Z"] 
}
```
*Note: `shortest_archive_path` should be a list of storage node names, ordered from the initial node to the final archive node.*

You must install any necessary Python packages (like `sqlite3` which is built-in) and successfully run the script for the database `"billing-db"`. Keep your final test run's output in `/home/user/report.json` so it can be verified.