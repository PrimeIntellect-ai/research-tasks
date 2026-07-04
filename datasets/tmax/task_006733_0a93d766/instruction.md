You are acting as a technical assistant for a compliance officer auditing an organization's internal systems. We need to analyze employee access patterns to identify instances where managers and their direct subordinates have accessed the exact same internal resources, which might indicate a compliance risk or credential sharing.

We have a SQLite database located at `/home/user/audit.db`.
It contains two tables:
1. `employees`
   - `emp_id` (INTEGER PRIMARY KEY)
   - `manager_id` (INTEGER) - refers to `emp_id` of their manager (can be NULL)
   - `name` (TEXT)
2. `access_logs`
   - `emp_id` (INTEGER)
   - `resource_id` (TEXT)
   - `access_count` (INTEGER) - number of times they accessed this resource

Your task is to write a C program that directly connects to this SQLite database, performs the necessary cross-query aggregations, and materializes a bipartite-like graph projection of "Manager-Subordinate Co-access". 

Requirements:
1. Create a C program at `/home/user/audit_graph.c`.
2. The program must use the SQLite3 C API (`sqlite3.h`) to read `/home/user/audit.db`.
3. The program must find all instances where a manager and their direct subordinate have accessed the *same* `resource_id`.
4. The program must materialize these relationships by writing them to a CSV file located at `/home/user/co_access_graph.csv`.
5. The output CSV must not have a header row and must strictly follow this format:
   `Manager_ID,Subordinate_ID,Resource_ID,Manager_Total_Accesses,Subordinate_Total_Accesses`
6. Sort the output in ascending order by `Manager_ID`, then `Subordinate_ID`, then `Resource_ID`.
7. Compile your program to `/home/user/audit_graph` and execute it to generate the CSV. You may need to install the SQLite3 development headers for C (`libsqlite3-dev`) via your package manager.

Ensure the final CSV precisely matches the requested format and sort order.