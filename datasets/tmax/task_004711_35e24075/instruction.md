You are acting as a compliance officer auditing an access control system. You have been provided with an SQLite database at `/home/user/audit.db` containing the system's role-based access control (RBAC) configurations and recent access logs.

System administrators have reported that the database contains a corrupted index on the `access_logs` table (`idx_logs_time`), which sometimes causes queries to return stale or omitted rows. 

Your objective is to write a Bash script at `/home/user/analyze_audit.sh` that automates the auditing process. The script must:
1. Ensure the `sqlite3` CLI tool is installed (if not, install it using `apt-get`).
2. Fix the corrupted index in `/home/user/audit.db` by executing a `REINDEX;` command before running any analysis.
3. Use a single complex SQLite query embedded in your Bash script to:
   - Use a **Recursive Common Table Expression (CTE)** to traverse the `role_inheritance` graph (resolving which roles inherit from which, all the way down the tree) to map every user to all their effective roles.
   - Map those effective roles to their granted `resource_name`s to build a comprehensive list of allowed permissions per user.
   - Join this effective permissions list against the `access_logs` table to find **invalid accesses** (where a user accessed a resource they do not have effective permission for).
   - Use **Window Functions** to rank these violations, extracting only the **2 most recent invalid accesses** per user based on the `timestamp`.
4. The output of the query must be saved to `/home/user/recent_violations.csv` in standard CSV format with a header row. 
   The columns must strictly be: `username,resource_name,timestamp` (ordered alphabetically by username, then descending by timestamp).

Database Schema details for `/home/user/audit.db`:
- `users`: `user_id` (INT), `username` (TEXT)
- `roles`: `role_id` (INT), `role_name` (TEXT)
- `user_roles`: `user_id` (INT), `role_id` (INT)
- `role_inheritance`: `parent_role_id` (INT), `child_role_id` (INT) - Note: A parent role inherits all permissions of its child roles.
- `role_permissions`: `role_id` (INT), `resource_name` (TEXT)
- `access_logs`: `log_id` (INT), `timestamp` (DATETIME), `user_id` (INT), `resource_name` (TEXT)

Ensure your script is executable and performs the complete pipeline when run without arguments.