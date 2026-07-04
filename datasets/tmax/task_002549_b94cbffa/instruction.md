You are acting as an automated compliance officer auditing internal systems. We need a reliable auditing script to check for Separation of Duties (SoD) risk scores based on an employee's access logs and assigned roles.

We have a custom graph risk-scoring utility provided by our security vendor located at `/app/sod-graph-checker-1.1.0/`. However, the security team reported that they couldn't compile it on this system due to a build error.

Your task is to:
1. Fix the build configuration for the vendored package `sod-graph-checker-1.1.0` and compile it so that the binary is produced at `/app/sod-graph-checker-1.1.0/bin/check_sod`.
2. Write a wrapper script at `/home/user/audit_user.sh` that takes a single user ID (`uid`) as a command-line argument.
3. The script must query the SQLite database at `/var/data/hr.db`. For the given `uid`, you must extract:
   - All roles directly assigned to the user (from `user_roles` joined with `roles`).
   - The user's top 3 most recently accessed resources where the status was 'GRANTED'. You MUST use a SQL window function (e.g., `ROW_NUMBER()`) over the `access_logs` table to find the top 3 latest distinct resources per user.
4. Your script must format this extracted data into the following precise JSON structure:
   ```json
   {
     "uid": <integer>,
     "roles": ["<role1>", "<role2>"],
     "recent_resources": [
       {"resource_id": "<res1>", "latest_access": "<timestamp>"},
       {"resource_id": "<res2>", "latest_access": "<timestamp>"}
     ]
   }
   ```
   (Sort `recent_resources` descending by `latest_access`. Output raw JSON, with no extraneous text).
5. Finally, your script must pipe this JSON directly into the standard input of the compiled `/app/sod-graph-checker-1.1.0/bin/check_sod` binary, and print only the binary's standard output to the console.

Ensure your script handles standard CLI execution: `bash /home/user/audit_user.sh <uid>`.