You are a Database Reliability Engineer (DBRE) managing a fleet of database backups. A legacy backup system dumps metadata into a raw CSV file, but this file often contains corrupted records, schema violations, and failed backup logs.

Your task is to write a C program that processes this raw relational data, validates the schema, filters for successful backups, and converts the data into a document-based JSON format that also includes parameterized SQL query constructions for a downstream restore automation system.

1. There is a CSV file located at `/home/user/backups.csv` with the header:
   `id,timestamp,db_name,status,size_bytes`

2. Write a C program at `/home/user/process_backups.c` that reads `/home/user/backups.csv`. You may only use the standard C library (`libc`). Do not use any external JSON or CSV parsing libraries.

3. The program must perform **Output schema validation** on each row (skipping the header):
   - `id`: Must be a valid positive integer.
   - `timestamp`: Must be a valid positive integer.
   - `db_name`: String containing only alphanumeric characters and underscores (max 50 chars).
   - `status`: Must be exactly "SUCCESS" or "FAILED".
   - `size_bytes`: Must be a valid integer.
   If a row violates any of these schema rules, completely ignore it.

4. Apply the following business filter:
   - Only process records where `status` is "SUCCESS" AND `size_bytes` is greater than `0`.

5. For the valid, filtered records, perform **Cross-representation mapping** and **Parameterized query construction**. Output the result as a valid JSON array to `/home/user/valid_backups.json`. 
   Each object in the JSON array must strictly match the following format exactly (whitespace formatting can vary, as long as it is valid JSON):
   ```json
   [
     {
       "document": {"id": 1, "ts": 1690000000, "db": "users_db", "bytes": 1048576},
       "sql_param_query": "INSERT INTO restored_backups (id, ts, db, bytes) VALUES (?, ?, ?, ?);",
       "sql_bind_args": ["1", "1690000000", "users_db", "1048576"]
     }
   ]
   ```
   *Note: `sql_param_query` is always the exact static string shown above, while `sql_bind_args` contains the string representations of the four fields extracted from the CSV.*

6. Compile your C program and run it to generate `/home/user/valid_backups.json`.