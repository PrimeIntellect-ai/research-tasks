You are a Database Reliability Engineer managing cross-system backups. An automated backup job recently exported a fragmented snapshot of your organization's file storage system across three different formats (Relational, Graph/Edges, and Document). 

You need to verify the integrity of these backups by mapping the entities across representations, summarizing the data, and designing an index strategy for the relational database.

The exported data is located in `/home/user/data/` (you will need to process these files):
1. **Relational:** `/home/user/data/users.sqlite` (SQLite3 Database)
   - Table: `users`
   - Schema: `id INTEGER PRIMARY KEY, name TEXT, department TEXT, status TEXT`
2. **Document:** `/home/user/data/docs.jsonl` (JSON Lines)
   - Format: `{"doc_id": "string", "size_bytes": integer, "type": "string"}`
3. **Graph/Edges:** `/home/user/data/access.csv` (CSV)
   - Format: `user_id,doc_id` (No header row)

Your tasks are to:

1. **Cross-Query Pipeline (Bash):** Write a bash script at `/home/user/analyze_backups.sh` that processes these three files using CLI tools (like `sqlite3`, `jq`, `awk`, etc.). The script must calculate the total document size (in bytes) owned by each user. 
   - When executed, the script must generate a tab-separated values (TSV) file at `/home/user/user_storage.tsv`.
   - The TSV must have exactly three columns: `user_name`, `department`, and `total_bytes`.
   - The output must be sorted by `total_bytes` in descending order. If there is a tie, sort by `user_name` in ascending alphabetical order.
   - Users with no documents should NOT be included in the output.

2. **Index Strategy Design:** The application heavily relies on the following SQL query to generate department rosters:
   `SELECT name FROM users WHERE department = ? AND status = 'active' ORDER BY name;`
   - Analyze this query and write a single, optimal SQLite `CREATE INDEX` statement to cover this query (avoiding full table scans and optimizing the sort).
   - Save this exact SQL statement to `/home/user/index_strategy.sql`. Name the index `idx_dept_status_name`.

Ensure your bash script is executable. You may run your script to verify your work.