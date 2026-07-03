You are acting as a compliance officer auditing an organization's access control systems. You have been provided with an SQLite database file at `/home/user/access_graph.db` containing an access graph.

The database contains two tables representing a directed graph of permissions:
1. `entities`: Contains nodes in the graph.
2. `relations`: Contains directed edges representing access grants (e.g., User -> Group, Group -> System, Group -> Group).

Your task is to write a Python script `/home/user/audit_query.py` that performs the following steps:
1. Connects to `/home/user/access_graph.db`.
2. Inspects the schema to understand how entities and relations are linked.
3. Automatically creates an optimal index (or indexes) on the `relations` table to speed up graph traversal queries (if they don't already exist).
4. Uses a Recursive Common Table Expression (CTE) to find all unique `System` type entities that a given `User` has access to, either directly or indirectly (via intermediate groups).
5. The username must be passed dynamically as a command-line argument to your script, and your query must use parameterized inputs to prevent SQL injection.
6. The query should filter the results to only include `System` entities, sort them alphabetically by their names, and paginate/limit the output to the top 5 results.
7. The script must write these top 5 System names (one per line) to `/home/user/report.txt`.

Once you have written the script, run it for the user `Alice` by executing:
`python3 /home/user/audit_query.py Alice`

Ensure that the output is accurately saved to `/home/user/report.txt` and that your script creates the necessary indexes in the database before running the query.