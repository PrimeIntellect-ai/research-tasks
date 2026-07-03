You are a compliance officer auditing an organization's internal network graph for suspicious access patterns. You have been provided with an SQLite database file located at `/home/user/audit_logs.db`. This database contains an unknown schema representing a graph of system accesses (e.g., actors, targets, time, risk scores, and context tags).

Your task is to write a C++ program that analyzes this access graph. 

Requirements:
1. **Reverse Engineer the Data Model:** You must first inspect `/home/user/audit_logs.db` to understand its schema, specifically looking for how events, actors, timestamps, risk scores, and context tags are stored.
2. **Parameterized Query Construction:** Write a C++ program in `/home/user/audit_analyzer.cpp`. The program must take exactly one command-line argument: a context tag (e.g., `PROD` or `DEV`). You must use the C++ `sqlite3` C-API (`libsqlite3`) to connect to the database and construct a securely parameterized SQL query that filters the data by this context tag.
3. **Window Functions & Analytical Aggregation:** For the filtered records, compute a rolling sum of the risk score for each actor. The rolling sum should be calculated over a window of the current access event and the preceding 2 events for that specific actor, ordered by the event timestamp (i.e., a maximum of 3 events per window).
4. **Determine Maximums:** For each actor, find their maximum rolling risk score across all their events in that context.
5. **Output:** Your C++ program must write the top 5 actors with the highest maximum rolling risk score to `/home/user/suspicious_users.log`, ordered by the maximum rolling risk score descending, then by actor name alphabetically.

The log file must be formatted exactly as follows for each line:
`Actor: <actor_name>, Max Rolling Risk: <score formatted to 2 decimal places>`

You can compile your program using:
`g++ -std=c++17 /home/user/audit_analyzer.cpp -lsqlite3 -o /home/user/audit_analyzer`

Once compiled, you must run your program with the context tag `PROD` to generate the log file.
`/home/user/audit_analyzer PROD`

Ensure `/home/user/suspicious_users.log` exists and contains the correct results when you are done.