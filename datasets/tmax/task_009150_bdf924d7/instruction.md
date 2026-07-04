You are an AI assistant helping a compliance officer audit system access logs. We need to identify potential compliance risks based on access frequency and flag them in our IAM graph database.

You have been provided with an SQLite database at `/home/user/audit.db` containing a table named `access_logs`. 
The table schema is: `access_logs(user_id TEXT, resource_id TEXT, access_time INTEGER)`. 
`access_time` is stored as a Unix epoch timestamp.

Your task is to:
1. Write a C++ program at `/home/user/audit_processor.cpp`.
2. The program must connect to `/home/user/audit.db` using the SQLite3 C/C++ API.
3. Use a SQL query with window functions to identify users who have had **more than 5 access events** (i.e., 6 or more) within any sliding window of **600 seconds** (10 minutes).
4. For every unique `user_id` that meets this anomaly condition, generate a Cypher query to flag the user in our graph database. The Cypher query must be exactly in this format:
   `MATCH (u:User {id: 'USER_ID'}) SET u.compliance_risk = true;`
   (Replace `USER_ID` with the actual user_id).
5. Output the resulting Cypher queries to a file at `/home/user/flag_queries.cypher`.
6. The queries in `/home/user/flag_queries.cypher` must be deduplicated (one query per flagged user) and sorted alphabetically by `user_id`, with each query on a new line.

Compile your program using `g++ -O2 /home/user/audit_processor.cpp -lsqlite3 -o /home/user/audit_processor` and run it to produce the output file.

Constraints:
- You must use C++ and SQLite3.
- The window function should evaluate the count of rows for a user where the `access_time` is between 600 seconds preceding the current row's `access_time` and the current row's `access_time` (inclusive).
- Ensure `/home/user/flag_queries.cypher` is strictly formatted as requested.