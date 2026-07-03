You are a compliance officer auditing an internal IT system for unauthorized access to sensitive servers. 

A local SQLite database exists at `/home/user/audit.db` which contains a snapshot of the corporate knowledge graph of permissions and a recent log of access events.

The database contains three tables:
1. `entities` (`id` INTEGER PRIMARY KEY, `name` TEXT, `type` TEXT, `is_sensitive` INTEGER)
   - `type` can be 'USER', 'GROUP', or 'SERVER'.
   - `is_sensitive` is 1 for sensitive servers, 0 otherwise.
2. `relationships` (`source_id` INTEGER, `target_id` INTEGER, `rel_type` TEXT)
   - Contains graph edges mapping permissions.
   - `rel_type` can be 'MEMBER_OF' (User -> Group) or 'HAS_ACCESS' (User -> Server, or Group -> Server).
3. `access_events` (`event_id` INTEGER PRIMARY KEY, `user_id` INTEGER, `server_id` INTEGER, `timestamp` DATETIME)

Your task is to write a C++ program at `/home/user/audit_checker.cpp` that connects to this SQLite database and identifies unauthorized accesses to *sensitive* servers. 

An access is considered **unauthorized** if a user accessed a sensitive server but does NOT have a path of permission in the knowledge graph. A user has permission if:
- The User has a direct 'HAS_ACCESS' relationship to the Server.
- OR the User has a 'MEMBER_OF' relationship to a Group, and that Group has a 'HAS_ACCESS' relationship to the Server.

Using C++ and the sqlite3 C API, execute a query that:
1. Filters for access events targeting sensitive servers.
2. Identifies which of these events lack a valid permission path in the relationship graph.
3. Groups these unauthorized events by User and Server.
4. Uses a SQL Window Function (`DENSE_RANK()`) to rank the users based on their total count of unauthorized accesses across the entire dataset (highest count gets rank 1).
5. Writes the output to `/home/user/unauthorized_report.csv` in the exact format: `user_name,server_name,unauthorized_attempts,rank_overall` (include a header row).

To complete this task:
1. Write the C++ source code to `/home/user/audit_checker.cpp`.
2. Compile it using `g++ -std=c++17 /home/user/audit_checker.cpp -lsqlite3 -o /home/user/audit_checker`.
3. Run the executable to produce the report.