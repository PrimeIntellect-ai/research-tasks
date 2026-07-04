You are acting as a technical assistant to a compliance officer. We are currently auditing our internal access control systems. 

We have an in-house auditing tool written in C (`/home/user/audit_tool.c`) that queries a SQLite database (`/home/user/audit.db`). The tool is supposed to take a username as a command-line argument and output a JSON array of all the roles that user possesses, writing it to `/home/user/compliance_report.json`.

However, the tool is currently broken. Due to a poorly written SQL query (an implicit cross join), it falsely reports that users have almost every role in the system. Furthermore, it completely fails to account for role hierarchies (roles inheriting other roles).

Your task:
1. Analyze the SQLite database schema in `/home/user/audit.db` to understand the data model (users, roles, direct user-role mappings, and role inheritance).
2. Fix the C program at `/home/user/audit_tool.c`. You must rewrite the SQL query to correctly fetch all roles for the specified user.
3. The new query *must* use a recursive Common Table Expression (CTE) to resolve the nested role hierarchy. If a user is granted Role A, and Role A inherits Role B, the user effectively has both Role A and Role B.
4. The C program must write the final resolved role names as a strictly formatted JSON array of strings to `/home/user/compliance_report.json`, sorted alphabetically. 
   Example format: `["admin", "developer", "viewer"]`
5. Compile your fixed tool using `gcc /home/user/audit_tool.c -lsqlite3 -o /home/user/audit_tool`.
6. Run your tool for the user `charlie`: `/home/user/audit_tool charlie`

Ensure the final `/home/user/compliance_report.json` contains exactly the correct JSON array for `charlie` and nothing else.