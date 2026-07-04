You are assisting a researcher who is organizing a large academic citation graph dataset. 

The dataset is stored in an encrypted SQLite database. Users frequently submit SQL queries to perform graph traversals and compute shortest paths. However, many of these submitted queries contain implicit cross joins (e.g., querying `FROM nodes n1, nodes n2` without a connecting edge condition). These poorly constructed queries cause massive Cartesian products that hang the database servers.

To mitigate this, we have provided a compiled, stripped binary at `/app/graph_oracle`. This binary has the database decryption key built-in and acts as a query planner. 
Usage: `/app/graph_oracle "<sql_query>"`
It outputs the SQLite `EXPLAIN QUERY PLAN` for the provided query against the underlying graph schema (which contains `nodes` and `edges` tables).

Your task is to create a robust Python sanitization script at `/home/user/sanitizer.py` that:
1. Takes a single SQL query string as its first command-line argument.
2. Uses parameterized execution or safe shell invocation to pass the query to `/app/graph_oracle`.
3. Interprets the resulting query plan.
4. Prints exactly `REJECT` to standard output if the query plan indicates a Cartesian product / implicit cross join (typically characterized by multiple full `SCAN TABLE` operations on the graph tables without corresponding `SEARCH` index lookups for the join).
5. Prints exactly `ACCEPT` to standard output if the query plan shows a properly constrained traversal (e.g., utilizing `SEARCH TABLE` on edges or valid recursive CTEs for shortest path computation).

You must deduce the exact schema and query plan formats by experimenting with the `/app/graph_oracle` binary. You are free to use standard reverse-engineering tools (`strings`, `objdump`) or treat it as a black-box oracle.

Ensure your script handles errors gracefully and prints only `ACCEPT` or `REJECT`.