You are acting as a compliance officer auditing an internal system. We suspect an insider threat and need to analyze access patterns. 

You have been provided with two pieces of evidence:
1. An organizational chart image at `/app/org_chart.png`. This image contains comma-separated lines indicating managerial relationships in the format `Manager,Employee`. You will need to extract this graph.
2. An SQLite database at `/app/audit.db` containing a table `access_logs` with schema `(id INTEGER PRIMARY KEY, username TEXT, access_time INTEGER)`. 

There is a known issue where the `idx_access_time` index in the database is corrupted, causing queries that use it to return stale or incomplete rows. You must bypass or drop this index to ensure accurate counts.

Your task is to write a C program that:
1. Parses the organizational hierarchy extracted from the image.
2. Queries the SQLite database (ensuring a full table scan, bypassing the corrupted index).
3. Starts a raw TCP server listening on `127.0.0.1:8888`.
4. When a client connects and sends a username followed by a newline (e.g., `Alice\n`), the server must calculate the total number of access log entries for that user AND all of their transitive subordinates (i.e., anyone in their management chain).
5. The server should respond with the total count as an integer followed by a newline (e.g., `42\n`) and then close the connection.

Requirements:
- You must write the solution in C. Standard POSIX libraries and `libsqlite3` are available. 
- You may use `tesseract` to extract the text from the image before running your C program, or invoke it via `system()` in your C code.
- Compile your program and leave it running in the background so it can be verified. Use port `8888`.
- Ensure your server can handle multiple sequential requests.

Example interaction:
Client sends: `Sarah\n`
Server responds: `15\n`
(Where 15 is the sum of accesses by Sarah and all employees under her).