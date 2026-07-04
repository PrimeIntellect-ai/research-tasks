You are a data engineer working on the extraction phase of a new ETL pipeline. You need to pull sensor telemetry data from a local SQLite database, optimize the retrieval process, and export the extracted data into a JSON format for downstream processing.

The database is located at `/home/user/telemetry.db`. 
It contains a single table:
`sensor_data` (
    `id` INTEGER PRIMARY KEY,
    `sensor_id` TEXT,
    `timestamp` TEXT,
    `reading` REAL,
    `status` TEXT
)

Your task consists of three parts:

1. **Index Strategy Design**
The downstream pipeline will frequently query this table by `status` and order the results by `timestamp` in descending order. 
Create an index named `idx_status_time` on the `sensor_data` table in `/home/user/telemetry.db` that optimizes this exact query pattern.

2. **C Extraction Program**
Write a C program located at `/home/user/etl_extract.c` that compiles to an executable named `/home/user/etl_extract`. 
The program must:
- Connect to `/home/user/telemetry.db` using the SQLite3 C API.
- Take exactly three command-line arguments after the program name: `<status>` `<limit>` `<offset>`.
- Execute a query to fetch the `id`, `sensor_id`, `timestamp`, and `reading` for rows matching the given `<status>`, ordered by `timestamp` descending.
- **Security Requirement:** You MUST use parameterized queries (prepared statements with `sqlite3_bind_*` functions) for the status, limit, and offset to prevent SQL injection.
- Export the results into a file named `/home/user/extract.json` as a valid JSON array of objects.

Example expected format for `/home/user/extract.json`:
```json
[
  {"id": 45, "sensor_id": "SENS-02", "timestamp": "2023-10-21T10:00:05Z", "reading": 102.40},
  {"id": 12, "sensor_id": "SENS-01", "timestamp": "2023-10-21T09:55:00Z", "reading": 98.10}
]
```
*(Ensure proper JSON formatting. You may manually construct the JSON strings using `printf`/`fprintf` since the text fields in the database do not contain any special characters or quotes).*

3. **Execution**
Compile your C code (don't forget to link the sqlite3 library).
Run your program to fetch the telemetry data where the status is `"ERROR"`, with a limit of `5` and an offset of `10`.

Ensure the final JSON file is created at `/home/user/extract.json`.