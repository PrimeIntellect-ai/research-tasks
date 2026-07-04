As a compliance officer auditing our internal networks, I need you to investigate a potential data exposure incident. 

We intercepted an automated voice alert regarding a suspicious user. You will find this recording at `/app/intercept.wav`. First, transcribe this audio to identify the target `user_id` (it will be spoken as a series of digits).

Once you have the `user_id`, investigate their lateral movement across our systems using the database at `/app/audit.db` (SQLite3). The database contains two tables:
1. `systems` (sys_id, ip_address, hostname)
2. `access_logs` (log_id, source_sys_id, dest_sys_id, user_id, timestamp, duration_seconds)

Write a Bash script at `/home/user/run_audit.sh` that accepts a `user_id` as its first argument and queries the database to find the shortest path of distinct systems this user traversed, starting from the system with hostname 'entry.corp.local'. 

Your script must:
1. Use a Recursive CTE to traverse the access graph.
2. Use window functions to calculate the cumulative `duration_seconds` along the path.
3. Output strictly valid JSON to stdout in this exact schema:
   `[{"path_length": <int>, "total_duration": <int>, "system_chain": ["entry.corp.local", "next.sys", ...]}]`
4. Run extremely fast. The database is quite large. You will need to interpret the query plan and create the necessary indexes in `/app/audit.db` to optimize the traversal. 

Your script's execution time will be measured. It must complete the graph traversal and JSON generation in under 0.5 seconds.