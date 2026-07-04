As a compliance officer, I need to audit our company's legacy access control system to identify potential unauthorized delegation paths. The legacy system's access mapping logic is locked inside an undocumented, stripped binary located at `/app/legacy_audit_tool`. 

I have extracted a list of all entity IDs (users, roles, and resources) into a file at `/app/entities.csv` (which contains one integer ID per line).

Your task is to:
1. Reverse-engineer or treat `/app/legacy_audit_tool` as an oracle. When executed with a single entity ID as a command-line argument (e.g., `/app/legacy_audit_tool 42`), it outputs the entity IDs that the given entity has direct access to.
2. Query the binary for every ID listed in `/app/entities.csv` to map out the complete directed graph of access rights.
3. Write a custom server in **C** that loads this mapped access graph into memory and listens for raw TCP connections on `127.0.0.1:8888`.
4. Your C server must handle incoming text-based queries over TCP. The requests will be strictly in the format: `CHECK <source_id> <target_id>\n`.
5. For each request, compute the shortest access path (fewest number of hops) from the `<source_id>` to the `<target_id>`. 
6. The server must respond with the exact path as a comma-separated string of IDs (including both source and target), followed by a newline. For example: `42,105,99\n`. If no path exists between the two entities, respond with `NONE\n`.
7. Compile your C program to `/home/user/audit_server`. Run it in the background so that it is actively listening on port `8888` when you finish.

Requirements:
- You must write the server in C.
- You may write auxiliary scripts (e.g., bash, python) to extract the data from the binary and format it into a file that your C server can easily read on startup.
- The server must support multiple sequential queries on the same connection, or close the connection after responding—either is fine as long as it correctly answers. 
- Ensure your C code handles basic network errors and doesn't crash on invalid input.