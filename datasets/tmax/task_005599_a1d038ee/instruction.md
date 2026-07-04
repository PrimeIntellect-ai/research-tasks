You are assisting a compliance officer in auditing system access records. The access matrix is modeled as a knowledge graph with nodes and edges. We need to identify Segregation of Duties (SoD) violations. Specifically, a violation occurs when a single `User` has both the ability to `can_request` access to a `System` and `can_approve` access to that same `System`, potentially through different `Role`s.

The graph data is provided in two CSV files:
1. `/home/user/nodes.csv` (columns: `id,type`)
   - `type` can be `User`, `Role`, or `System`.
2. `/home/user/edges.csv` (columns: `source,target,relation`)
   - `relation` can be `has_role`, `can_request`, or `can_approve`.

Your task:
1. Write a C program at `/home/user/audit_graph.c` that uses the SQLite3 C API (`sqlite3.h`).
2. The program must create a new SQLite database file at `/home/user/audit.db`.
3. Create two tables: `nodes(id TEXT, type TEXT)` and `edges(source TEXT, target TEXT, relation TEXT)`.
4. Read the data from the CSV files and insert it into the tables.
5. Create necessary indexes on the `edges` and `nodes` tables to optimize graph traversal and pattern matching.
6. Execute a SQL query (using complex joins) to find all SoD violations. A violation is defined by the exact graph pattern:
   - `User` -[has_role]-> `Role_A` -[can_request]-> `System`
   - AND `User` -[has_role]-> `Role_B` -[can_approve]-> `System`
   (Note: `Role_A` and `Role_B` can be the same role or different roles).
7. Write the results to `/home/user/violations.log` in the format `UserID,SystemID`. Each violation should be on a new line. Sort the output alphabetically by `UserID`, then `SystemID`.
8. Compile your program using `gcc -o /home/user/audit_graph /home/user/audit_graph.c -lsqlite3` and run it.

Ensure your program handles errors gracefully and correctly closes the database. Do not use external libraries other than standard C libraries and `sqlite3`.