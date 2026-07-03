You are acting as a Database Administrator and Go Developer. We have a Go application located at `/home/user/app/main.go` that queries a SQLite database located at `/home/user/app/company.db`.

The application is supposed to retrieve a hierarchical list of all subordinates (direct and indirect) under the CEO (Employee ID = 1), including the CEO themselves, along with their assigned projects. 

Currently, the SQL query in `main.go` has a severe bug: it uses an implicit cross join when joining the recursive CTE with the projects table. This produces incorrect, duplicate-filled results and causes terrible performance. Furthermore, the database schema lacks necessary indexes for the hierarchical traversal and project lookups.

Your tasks are to:
1. Initialize a Go module in `/home/user/app` and install the SQLite driver (`github.com/mattn/go-sqlite3`).
2. Fix the SQL query in `/home/user/app/main.go`. Use a recursive CTE to find employee ID 1 and all their direct/indirect subordinates. Correctly join the `projects` table so each employee is linked ONLY to their actual projects. You must use a `LEFT JOIN` so that employees without projects are still included in the result (their project name should be handled as an empty string `""` in the Go struct).
3. Connect to the SQLite database `/home/user/app/company.db` (e.g., via the `sqlite3` CLI) and create necessary indexes to optimize the query plan. Specifically, you must create an index on the `manager_id` column of the `employees` table, and an index on the `employee_id` column of the `projects` table.
4. Update `main.go` to execute the query and write the result as a JSON array to `/home/user/app/results.json`. The output must be an array of objects matching this schema: `[{"employee_name": "string", "project_name": "string"}]`.
5. Extract the query execution plan to demonstrate query plan interpretation. Run an `EXPLAIN QUERY PLAN` on your newly fixed query (using `1` for the target ID) using the `sqlite3` CLI, and redirect the output to `/home/user/app/plan.txt`.

Ensure your Go application compiles and runs successfully, outputting the correct JSON file.