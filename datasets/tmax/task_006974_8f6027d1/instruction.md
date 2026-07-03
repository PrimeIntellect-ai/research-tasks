You are a data engineer building an ETL pipeline to migrate human resources data from a legacy relational event-store into a Graph Database, to enable better organizational network analysis.

You have been provided with an SQLite database at `/home/user/hr_data.db`. It contains a single table:
`emp_events (event_id INTEGER PRIMARY KEY, emp_id INTEGER, manager_id INTEGER, salary REAL, dept TEXT, event_timestamp DATETIME)`

This table is an append-only event log. Every time an employee changes roles, salaries, or managers, a new row is inserted. 

Your task is to write a C++ program `/home/user/convert.cpp` that reads this SQLite database, computes the *current* active snapshot of the organization, and outputs a Cypher script to load this data into a graph database.

Requirements for `/home/user/convert.cpp`:
1. Use the SQLite3 C/C++ API (`sqlite3.h`). You can install necessary dev packages using `sudo apt-get update && sudo apt-get install -y libsqlite3-dev`.
2. Connect to `/home/user/hr_data.db`.
3. Execute a SQL query that uses **Window Functions** to retrieve only the *latest* event (by `event_timestamp`) for each `emp_id`. Ignore events where the employee has been terminated (indicated by `manager_id` being `-1`).
4. Generate a Neo4j Cypher script and save it exactly to `/home/user/import.cypher`.
5. For each active employee in the latest snapshot, generate the following exact Cypher commands (replace bracketed items with actual values):
   ```cypher
   MERGE (e:Employee {id: [emp_id]}) SET e.salary = [salary], e.dept = '[dept]';
   MERGE (m:Employee {id: [manager_id]});
   MERGE (e)-[:REPORTS_TO]->(m);
   ```
6. The generated commands in `/home/user/import.cypher` must be ordered by `emp_id` in ascending order. Write the 3 commands for a single `emp_id` consecutively on separate lines, followed by a blank line, before moving to the next `emp_id`.

Compile your code to `/home/user/convert` and run it so that `/home/user/import.cypher` is produced.

To complete the task, leave the compiled `/home/user/convert` binary and the generated `/home/user/import.cypher` on the file system.