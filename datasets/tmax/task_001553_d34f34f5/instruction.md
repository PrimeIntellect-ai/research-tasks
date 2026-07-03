You are acting as a data engineer tasked with building a custom ETL pipeline in C. We are migrating data from a legacy relational system into a modern graph database. 

You have been provided with an SQLite database at `/home/user/legacy.db` (which you must assume exists, but you will need to discover its exact schema). 
The database contains three undocumented tables: `t_alpha`, `t_beta`, and `t_gamma`. Through reverse engineering, you must determine how these tables relate to represent Users, their Posts, and their Connection Networks.

Your objective is to write a C program at `/home/user/etl_extract.c` that does the following:

1. Connects to `/home/user/legacy.db` using the SQLite3 C API.
2. Creates the optimal indexes on the tables to speed up complex queries (this tests query plan optimization, as the database is initially unindexed and large).
3. Executes a single, complex SQL query (involving joins and subqueries) to extract pairs of connected users who have a specific interaction pattern. Specifically, extract pairs of users (User1, User2) where:
   - User1 and User2 are connected in the network table (`t_gamma`).
   - User1 has created at least one post in `t_beta` that was published after 2022-01-01.
   - User2 has created at least one post in `t_beta` that was published after 2022-01-01.
4. Translates these extracted relationships into a Cypher query format for our new graph database.
5. Writes the output to `/home/user/graph_import.cypher`.

The output file `/home/user/graph_import.cypher` must contain strictly formatted Cypher `CREATE` statements, one per line, ordered chronologically by User1's ID, then User2's ID (ascending).
Format for each line:
`CREATE (u1:User {id: <User1_ID>})-[:CONNECTED_ACTIVE]->(u2:User {id: <User2_ID>})`

Requirements:
- Install any necessary C development libraries for SQLite3 (e.g., `libsqlite3-dev`).
- Compile your program to `/home/user/etl_extract`.
- Execute it to produce the `.cypher` file.
- Do not hardcode the IDs in your C program; it must dynamically execute the query.