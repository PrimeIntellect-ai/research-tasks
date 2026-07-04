You are acting as a Database Administrator working with a relational graph database.

You have been given an SQLite database at `/home/user/graph.db` containing a social graph of employees.
The database has two tables:
1. `users`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `department` (TEXT)
2. `connections`: `u1` (INTEGER), `u2` (INTEGER), `weight` (INTEGER)

Note on `connections`: Every connection is stored exactly once, ensuring `u1 < u2`.

A previous developer wrote a SQL query to find the top 5 most strongly connected "triangles" of users within the 'Engineering' department. A triangle exists if there are connections between User A and User B, User B and User C, and User A and User C. The strength of a triangle is the sum of the weights of these three connections. 

The developer's query is saved at `/home/user/bad_query.sql`. It is currently very slow and returns completely incorrect results due to an implicit cross-join bug.

Your task:
1. Identify and fix the bug in the SQL query. The query should correctly find all triangles in the 'Engineering' department (`u1 < u2 < u3`).
2. Order the results by the total weight of the triangle in descending order. If there is a tie, order by the first user's ID ascending, then the second user's ID ascending, then the third user's ID ascending.
3. Limit the results to the top 5 triangles.
4. Execute your corrected query against `/home/user/graph.db` and output the results to `/home/user/top_5_triangles.csv`. The CSV must have the header row: `u1_id,u2_id,u3_id,total_weight`.
5. Run `EXPLAIN QUERY PLAN` on your corrected query and save the raw output to `/home/user/query_plan.txt`.

Do not modify the database schema or data. Only create the two requested output files.