You are assisting a compliance officer in auditing an internal communications network for suspicious activity. The current audit tool, written in C and backed by a SQLite database, is failing. It takes far too long to run and produces millions of false positive records. 

An initial investigation suggests the SQL query inside the tool contains an implicit cross join (Cartesian product) instead of correctly linking the tables. 

Here is the setup of the system you are working with:
- The database is located at `/home/user/audit.db`.
- The database schema consists of two tables:
  `employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT)`
  `messages (id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, timestamp DATETIME, flagged INTEGER)`
- The C program source code is located at `/home/user/audit_tool.c`.

Your objectives are as follows:

1. **Fix the Query (C Programming & SQL):**
   Modify `/home/user/audit_tool.c` to fix the SQL query. The query should return all flagged messages (`flagged = 1`) where *both* the sender and the receiver are in the `'Finance'` department. The query must correctly join the `employees` table to the `messages` table for both the sender and the receiver (no cross joins!). It should select `sender_name`, `receiver_name`.

2. **Index Strategy (Optimization):**
   Create a SQL script at `/home/user/optimize.sql` containing `CREATE INDEX` statements to optimize your new query. You must index the tables to prevent full table scans on the `messages` and `employees` tables during this specific query. Apply these indexes to the `/home/user/audit.db` database.

3. **Query Plan Extraction:**
   Extract the execution plan for your optimized query using SQLite's `EXPLAIN QUERY PLAN` command and save the exact output to `/home/user/query_plan.txt`.

4. **Graph Analytics (Centrality):**
   Extend the C program in `/home/user/audit_tool.c` so that after fetching the correctly filtered records, it calculates the "degree centrality" for each employee in the resulting suspicious Finance network. Degree centrality here is defined as the total number of flagged messages an employee either sent OR received within this specific filtered group.
   The C program must write the exact name of the employee with the highest degree centrality to a file named `/home/user/highest_centrality.txt` (just the name, no extra text).

Compile your fixed C program to `/home/user/audit_tool` (e.g., `gcc /home/user/audit_tool.c -o /home/user/audit_tool -lsqlite3`) and execute it to generate the final output file.