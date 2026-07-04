You are an AI assistant helping a compliance officer conduct a security audit. 

We suspect that some previously terminated employees (whose accounts are marked as REVOKED) might still have indirect access to highly sensitive systems through active service accounts and inherited group permissions. 

You have been provided with an SQLite database at `/home/user/audit.db` containing the current identity and access management (IAM) graph. 

The database has two tables:
1. `Entities`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (VARCHAR)
   - `type` (VARCHAR) - Can be 'USER', 'SERVICE_ACCOUNT', 'GROUP', 'DATA_LAKE', or 'FINANCE_DB'.
   - `status` (VARCHAR) - Can be 'ACTIVE' or 'REVOKED'.

2. `AccessGrants`
   - `source_id` (INTEGER) - The entity that holds the access.
   - `target_id` (INTEGER) - The entity being accessed or inherited.
   - `status` (VARCHAR) - Can be 'ACTIVE' or 'INACTIVE'.

**Your Objective:**
Write a Bash script at `/home/user/analyze_audit.sh` that analyzes the IAM graph to find all unauthorized paths. 

The script must:
1. Use a single SQLite query with a Recursive Common Table Expression (CTE) to traverse the access graph.
2. Start the traversal from any `Entities` where `type = 'USER'` and `status = 'REVOKED'`.
3. Follow only `AccessGrants` where the grant `status = 'ACTIVE'`.
4. Stop when the traversal reaches a highly sensitive system (where `Entities.type` is either `'DATA_LAKE'` or `'FINANCE_DB'`).
5. Calculate the exact number of hops (edges traversed) between the revoked user and the sensitive system.
6. Output the results to `/home/user/compromise_report.csv`.

**Requirements for the output file (`/home/user/compromise_report.csv`):**
- Must include a header row: `Source_User,Target_Entity,Hops`
- `Source_User` is the `name` of the revoked user.
- `Target_Entity` is the `name` of the sensitive system reached.
- `Hops` is the integer number of active access grants traversed.
- The output must be sorted first by `Hops` (ascending), then by `Source_User` (alphabetically ascending), and finally by `Target_Entity` (alphabetically ascending).

Make sure the bash script is executable. You can run the script and check the output to verify your work.