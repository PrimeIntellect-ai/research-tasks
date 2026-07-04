You are acting as a technical assistant to a compliance officer. We are auditing system access across our engineering organization. Access permissions are modeled as a graph in an SQLite database located at `/home/user/compliance.db`. The graph connects Users to Roles, and Roles to Systems.

Our automated bash script `/home/user/generate_audit.sh` is supposed to materialize a direct mapping (a bipartite graph projection) of Users to the Systems they can access. However, the current script triggers massive compliance alerts because the SQL query inside it contains a flawed implicit cross join, incorrectly reporting that every user has access to almost every system.

Your task is to:
1. Analyze the schema of `/home/user/compliance.db` to understand the relationships between `users`, `user_roles`, `role_systems`, and `systems`.
2. Fix the SQL query inside the bash script `/home/user/generate_audit.sh` so that it correctly traverses the graph (User -> Role -> System) without cross joins.
3. The script must execute the query using `sqlite3` and output the results directly to `/home/user/fixed_audit_report.csv`.
4. The CSV output must contain exactly two columns: `user_name` and `system_name` (in that order), with no header row.
5. The output in the CSV must be sorted alphabetically by `user_name` ascending, and then by `system_name` ascending.

Execute whatever commands are necessary to explore the database, fix the script, and run it to produce the correct `/home/user/fixed_audit_report.csv`.