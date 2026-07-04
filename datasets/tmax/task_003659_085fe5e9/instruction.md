You are a compliance officer auditing an organization's system access logs. The logs and system hierarchy have been ingested into an SQLite database representing a knowledge graph, located at `/home/user/sys_audit.db`.

The database contains two tables:
- `nodes` (id INTEGER PRIMARY KEY, type TEXT, name TEXT)
  - `type` can be 'User', 'Department', or 'Resource'.
- `edges` (source INTEGER, target INTEGER, relation TEXT)
  - `relation` can be 'MEMBER_OF' (User -> Department), 'BELONGS_TO' (Resource -> Department), or 'ACCESSED' (User -> Resource).

Due to a recent system crash, the indexes on the `edges` table are known to be corrupted and returning stale rows. 

Your task is to write a Bash script at `/home/user/audit_pipeline.sh` that performs the following:
1. Executes the `REINDEX;` command on the database to fix the corrupted indexes.
2. Constructs a SQL query to perform pattern matching on the graph to find **cross-department access violations**. A violation occurs when a User has 'ACCESSED' a Resource, and that Resource 'BELONGS_TO' a Department, but the User is **not** a 'MEMBER_OF' that same Department.
3. Chains the output of the SQLite query into a pipeline using `jq` to construct and validate the output schema. 
4. The final output must be saved to `/home/user/violations.json`. It must be a valid JSON array of objects, sorted alphabetically by the `user` field, and then by the `resource` field.
5. Each JSON object must strictly match this schema (keys must be exactly as written):
   - `user`: The name of the User.
   - `resource`: The name of the Resource accessed.
   - `resource_department`: The name of the Department the Resource belongs to.

Ensure your Bash script is executable (`chmod +x /home/user/audit_pipeline.sh`). You do not need to install any external validators; using standard `sqlite3` and `jq` in a pipeline is sufficient. Run your script to generate the `/home/user/violations.json` file.