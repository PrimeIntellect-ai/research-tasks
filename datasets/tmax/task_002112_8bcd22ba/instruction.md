You are assisting a compliance officer in auditing an internal communication database to detect potential data exfiltration. The system logs have been exported into an SQLite database located at `/home/user/audit.db`.

The database has the following schema:
- `employees`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `department` (TEXT)
- `communications`: `id` (INTEGER PRIMARY KEY), `sender_id` (INTEGER), `receiver_id` (INTEGER), `timestamp` (DATETIME), `byte_size` (INTEGER)

Your task is to analyze this data using C and SQLite, applying graph analytics concepts (specifically out-degree centrality) to find suspicious contractors. 

Perform the following steps:
1. **Index Optimization**: Analyze the schema and create optimal indexes to speed up joining and filtering by `sender_id` and `receiver_id`. Save the SQL statements you used to create these indexes in `/home/user/indexes.sql`.
2. **C Program Implementation**: Write a C program at `/home/user/audit_analyzer.c` that uses the `sqlite3` C library to perform cross-query aggregation. The program must:
   - Calculate the "out-degree" for each employee (the number of *unique* receivers they have sent communications to).
   - Calculate the total bytes sent by each employee.
   - Filter for employees whose `department` is exactly `'Contractor'` AND who have an out-degree strictly greater than `3` (which is suspicious for external contractors in this network).
3. **Execution and Output**: Compile your program (e.g., `gcc /home/user/audit_analyzer.c -o /home/user/audit_analyzer -lsqlite3`) and run it. The program must generate two output files:
   - `/home/user/flagged_contractors.txt`: A CSV formatted list of the flagged employees. Format: `EmployeeID,Name,OutDegree,TotalBytesSent`. Each record on a new line.
   - `/home/user/audit_summary.txt`: A two-line summary of the findings in the exact format:
     ```
     Total Suspicious Contractors: <COUNT>
     Max OutDegree: <MAX_OUT_DEGREE_AMONG_FLAGGED>
     ```

Make sure your C program handles potential SQLite errors gracefully.