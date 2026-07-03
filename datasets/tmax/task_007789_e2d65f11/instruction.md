You are acting as a compliance officer auditing a corporate Linux system. A recent security incident revealed that unauthorized employees might have access to restricted resources due to complex, deeply nested group memberships. 

You have been given access to an undocumented SQLite database file located at `/home/user/corp_audit.db` which contains the access control lists, user information, and resource mappings.

Your task is to:
1. Reverse engineer the schema of `/home/user/corp_audit.db` using the `sqlite3` CLI tool.
2. Write a Bash script at `/home/user/audit_path.sh` that takes exactly two arguments: a `username` (Argument 1) and a `resource_name` (Argument 2).
3. The script must securely query the SQLite database using Common Table Expressions (WITH RECURSIVE) to trace how a user inherits access to a resource through group memberships and nested group hierarchies.
4. The script should output the access path to standard output strictly in the following format:
   `Employee:<username> -> Group:<group_name> -> ... -> Group:<group_name> -> Resource:<resource_name>`
   If multiple paths exist, output the path with the fewest number of group hops.
   If no access path exists, the script must output exactly: `NO_ACCESS`

Once you have written and tested your script, use it to evaluate two specific scenarios and save the exact output of each run to a log file located at `/home/user/audit_results.txt` (one result per line):
- Scenario A: Check access for username `Mallory` to resource `Project_Apollo_Secrets`.
- Scenario B: Check access for username `Bob` to resource `Public_Share`.

Constraints:
- You must use Bash and the `sqlite3` command line tool.
- Do not install any additional packages; standard tools available in a standard Linux environment are sufficient.
- The SQLite query constructed in your script must dynamically use the provided script parameters.