I am a database administrator trying to optimize our graph materialization pipeline. We have a C++ application that connects to an SQLite database (`/home/user/graph.db`) containing a social network. The application is supposed to project and materialize a "second-degree friend" graph. 

However, the current SQL query inside `/home/user/project_graph.cpp` is severely broken. It has an implicit cross join that causes a massive explosion of incorrect rows, it lacks proper sorting, and it attempts to load everything into memory at once, crashing on larger datasets.

Your task is to fix the C++ application and the SQL query to meet the following strict requirements:

1. **Graph Projection & Filtering**: 
   - Modify the query to find all second-degree connections: User A is a friend of User B, and User B is a friend of User C (i.e., A -> B -> C).
   - Both edges must have `type = 'friend'`.
   - **Filter 1**: Exclude cases where A = C (a user cannot be their own second-degree friend).
   - **Filter 2**: Exclude cases where a direct 'friend' edge already exists between A and C.

2. **Result Sorting**:
   - The query results must be strictly ordered by the source user's ID in ascending order, followed by the target user's ID in ascending order.

3. **Pagination in C++**:
   - Do not fetch all rows at once. You must implement pagination directly in the C++ code by dynamically modifying the query to use `LIMIT 5 OFFSET ?`. 
   - Loop and fetch 5 rows at a time until no more rows are returned.

4. **Output Schema Validation**:
   - The C++ program must write the results to `/home/user/output.csv`.
   - The file must have exactly this header: `src,dst`
   - Followed by the correctly projected edges, formatted as `integer,integer`.

5. **Execution Plan**:
   - To prove the query no longer relies on a massive cross join, write your final fixed SQL query to a file named `/home/user/fixed_query.sql`.
   - Run SQLite's `EXPLAIN QUERY PLAN` on your fixed query and save the raw output to `/home/user/query_plan.txt`.

The database schema is as follows:
- `Nodes (id INTEGER PRIMARY KEY, name TEXT)`
- `Edges (src INTEGER, dst INTEGER, type TEXT)`

The buggy C++ file `/home/user/project_graph.cpp` and the database `/home/user/graph.db` are already in your home directory. You can compile the C++ code using `g++ -O3 /home/user/project_graph.cpp -lsqlite3 -o /home/user/project_graph`. 

Fix the code, compile it, run it to generate `/home/user/output.csv`, and create the `/home/user/query_plan.txt` log.