You are a compliance officer auditing a legacy access control system. 

We have an SQLite database located at `/home/user/audit.db`. Due to a recent storage failure, the primary index on the logging table became corrupted and returns stale or incomplete rows when queried normally, causing our standard auditing tools to fail.

Your task is to write a standalone C program that bypasses the issue and extracts the necessary compliance data.

Requirements:
1. Reverse engineer the schema of the database to find the table containing access logs (it contains employee IDs, actions, and timestamps).
2. Write a C program at `/home/user/audit_extractor.c` that connects to `/home/user/audit.db` using the SQLite3 C API (`sqlite3.h`).
3. Your C program must execute a query that uses a SQL **Window Function** to find the single *most recent* 'DENIED' action for each employee. 
4. To avoid the corrupted index, your SQL query must explicitly force a full table scan (e.g., using the `NOT INDEXED` clause on the table).
5. The C program should output the results in CSV format exactly as follows: `employee_id,timestamp` directly to a file named `/home/user/compliance_report.csv`.
6. Compile your program using `gcc` and run it to produce the final CSV.

Expected Output Format in `/home/user/compliance_report.csv`:
```csv
E001,2023-10-15 08:32:11
E002,2023-10-14 19:12:05
...
```
Order the final CSV output alphabetically by `employee_id`. Ensure the compilation and execution commands are standard Linux bash commands.