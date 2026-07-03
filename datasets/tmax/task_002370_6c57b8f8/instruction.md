You are a Database Reliability Engineer (DBRE) tasked with fixing a broken backup reporting pipeline. 

Recently, the automated backup size report started reporting astronomically high numbers and duplicate entries. We suspect the previous engineer wrote a SQL query containing an implicit cross join, but they left the company before documenting the schema.

Additionally, a voice message was left by the lead architect regarding a critical filter that must be applied to these reports, which is located at `/app/incident_report.wav`. 

Your task is to write a Python CLI tool that interrogates the database, correctly joins the tables, applies the analytical filtering, and exports the results.

Requirements:
1. Listen to / transcribe the audio file at `/app/incident_report.wav` to discover the specific `region` filter that must be applied to the storage nodes.
2. Reverse engineer the schema of the SQLite database currently provided at `/app/backups.db`. The database contains tables related to `clusters`, `storage_nodes`, and `backup_logs`.
3. Create a Python script at `/home/user/get_latest_backups.py`.
4. The script must take exactly one argument: the path to a SQLite database file.
   Example usage: `python3 /home/user/get_latest_backups.py /app/backups.db`
5. The script must execute a query that fixes the implicit cross join between nodes and logs.
6. Using a SQL Window Function (`ROW_NUMBER()` or similar), extract ONLY the most recent successful backup (where `status = 'SUCCESS'`) for each `database_name` on each `node_name`.
7. Filter the nodes based on the region mentioned in the audio file.
8. The script must print a JSON array of objects to standard output (stdout), with exactly the following keys: `node_name`, `database_name`, `backup_size_mb`, and `backup_timestamp`. 
9. Sort the JSON array alphabetically by `node_name` ascending, and then by `database_name` ascending.

Your script will be tested against a hidden oracle. We will run your script against several newly generated databases with the exact same schema but different data to ensure your SQL logic, window functions, and relationships are structurally correct. You must ensure bit-exact output equivalence to the oracle's JSON output.