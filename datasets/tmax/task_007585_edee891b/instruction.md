You are assisting a compliance officer who is auditing an access control system. The system's state is stored in an SQLite database located at `/home/user/audit.db`. Recently, a system crash suspectedly corrupted several database indexes, causing some queries to return stale or incomplete rows. 

Your task is to write a C program that repairs the database indexes, efficiently traverses the access control graph, and projects the effective permissions for a specific user.

Here is the schema of the database:
- `users` (user_id INTEGER PRIMARY KEY, username TEXT)
- `roles` (role_id INTEGER PRIMARY KEY, role_name TEXT)
- `user_roles` (user_id INTEGER, role_id INTEGER)
- `role_inheritance` (parent_role_id INTEGER, child_role_id INTEGER) -- "child_role_id" inherits all permissions of "parent_role_id"
- `role_permissions` (role_id INTEGER, permission_name TEXT)

Task requirements:
1. Write a C program at `/home/user/audit_resolver.c`.
2. The program must connect to `/home/user/audit.db` using the SQLite3 C API.
3. First, the program must execute a `REINDEX;` command to fix any potentially corrupted indexes.
4. Next, it must use a `WITH RECURSIVE` Common Table Expression (CTE) to traverse the role hierarchy and resolve ALL inherited and direct permissions for the user named exactly `'Charlie_Compliance'`. Note that inheritance is transitive (if A inherits from B, and B inherits from C, A gets C's permissions).
5. The program must write the final resolved, unique `permission_name`s to `/home/user/charlie_permissions.txt`. Each permission should be on a new line, sorted in ascending alphabetical order.
6. Install any necessary dependencies (like `libsqlite3-dev` and `gcc`), compile your C program to `/home/user/audit_resolver`, and execute it.

Ensure your program handles basic error checking (e.g., if the database fails to open) and successfully produces the final output file.