You are a database administrator tasked with optimizing a slow query on a generic graph database implemented in SQLite. 

A developer wrote a Bash wrapper script located at `/home/user/find_mutual.sh`. It queries an SQLite database at `/home/user/graph.db` to find "similar users" based on mutual follows. 

The database uses a generic graph schema, but there's no documentation. You will need to reverse-engineer the schema of `/home/user/graph.db` to understand how nodes and edges are stored, and specifically how "User" nodes and "FOLLOWS" edges are represented.

The developer's script is supposed to take three arguments:
`./find_mutual.sh <target_user_id> <limit> <offset>`

It should output the IDs of other users who follow at least one of the exact same users that the `<target_user_id>` follows, along with the count of mutual follows. 
The output must be formatted as comma-separated values (`similar_user_id,mutual_count`) and strictly ordered by `mutual_count` descending, and then by `similar_user_id` ascending to break ties. It must apply the specified limit and offset for pagination.

Your task is to:
1. Reverse-engineer the data model in `/home/user/graph.db`.
2. Optimize the database by creating necessary indexes to speed up the query.
3. Completely rewrite `/home/user/find_mutual.sh` using `sqlite3` to correctly implement the graph traversal, sorting, filtering, and pagination.
4. Export the `EXPLAIN QUERY PLAN` of your new, optimized SQL query (substituting 'U1', 10, 0 for the parameters) into a file at `/home/user/query_plan.txt`.

Ensure your rewritten Bash script is executable and prints exactly the expected rows to standard output.