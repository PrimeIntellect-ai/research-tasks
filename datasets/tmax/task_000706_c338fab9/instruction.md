You are a database administrator tasked with optimizing a knowledge graph database that models a corporate IT infrastructure. 

An unoptimized SQLite database is located at `/home/user/graph.db`. It contains information about servers, databases, and applications, as well as their dependencies. 

A developer has written a query to perform a knowledge graph pattern match (finding the cascading impact domain if a specific critical database fails) and saved it at `/home/user/query.sql`. However, the query is performing full table scans and is incredibly slow.

Your task:
1. Reverse engineer the data model of `/home/user/graph.db` to understand the tables and relationships.
2. Interpret the query plan for `/home/user/query.sql` using SQLite's `EXPLAIN QUERY PLAN`.
3. Design and implement an indexing strategy directly in `/home/user/graph.db` that optimizes the query. You must add the necessary indexes so that the query plan for `/home/user/query.sql` uses `SEARCH TABLE` instead of `SCAN TABLE` for all operations involving the main entities and relations tables.
4. Execute the query in `/home/user/query.sql` against the database and save the raw output (just the list of affected application names, one per line) to `/home/user/impact.txt`.
5. Create a bash script at `/home/user/verify_plan.sh` that, when executed, outputs the `EXPLAIN QUERY PLAN` of the query to stdout.

Requirements:
- Ensure the database file `/home/user/graph.db` is updated with your new indexes.
- Do not modify the contents of `/home/user/query.sql`.
- `/home/user/impact.txt` must contain exactly the names of the impacted applications, sorted alphabetically. You may need to append `ORDER BY` in your command-line execution (but do not modify the original `.sql` file).