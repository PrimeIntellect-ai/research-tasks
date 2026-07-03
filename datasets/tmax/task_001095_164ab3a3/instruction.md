You are a database administrator tasked with fixing a broken query in a C++ application.

We have a SQLite database at `/home/user/org_chart.db` containing a single table:
`nodes(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, role TEXT)`

This table represents a hierarchical organization chart. The C++ application at `/home/user/fetch_team.cpp` is supposed to retrieve all direct and indirect descendants of the employee named 'Alice'. However, the SQL query inside the C++ file is currently broken—it performs a buggy implicit cross join and does not properly recurse through the hierarchy.

Your task is to:
1. Modify `/home/user/fetch_team.cpp` to replace the broken query with a correct one. 
2. The new query must use a Recursive Common Table Expression (CTE) to find all descendants of 'Alice' (excluding 'Alice' herself).
3. The query must SELECT `id`, `name`, and `role`, and order the final results by `id` ascending.
4. Compile the C++ program using `g++ /home/user/fetch_team.cpp -lsqlite3 -o /home/user/fetch_team` and run it. The C++ program will automatically write the results to `/home/user/team_output.txt` in CSV format.
5. To demonstrate query plan interpretation, run `EXPLAIN QUERY PLAN` on your newly written recursive query using the `sqlite3` CLI against `/home/user/org_chart.db`. Save the verbatim output of this explain command to `/home/user/query_plan.txt`.

Ensure both `/home/user/team_output.txt` and `/home/user/query_plan.txt` exist and are correct before concluding.