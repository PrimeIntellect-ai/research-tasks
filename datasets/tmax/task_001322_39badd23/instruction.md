As a compliance officer auditing our internal systems, I need to verify user access rights against actual usage logs. We use a microservice architecture where our Role-Based Access Control (RBAC) data is stored in PostgreSQL, and our high-throughput access logs are stored in Redis.

We have a partially built Python Flask API located in `/home/user/audit_api/` that is supposed to serve compliance reports. Currently, the `/audit` endpoint is unimplemented. Your task is to implement this endpoint, properly query the databases, and ensure the API runs on port 8080.

### Database Architectures

**PostgreSQL (Credentials: postgres / password / db: rbac_db / port: 5432)**
Contains our RBAC schema:
- `users` (id, username)
- `roles` (id, role_name, parent_role_id) -> *Note: Roles can inherit permissions from a parent role. This hierarchy can be up to 5 levels deep.*
- `permissions` (id, resource_name)
- `role_permissions` (role_id, permission_id)
- `user_roles` (user_id, role_id)

**Redis (Localhost, Port: 6379, No Password)**
Contains access logs. Every time a user accesses a resource, an entry is added to a Sorted Set.
- Key format: `access:<resource_name>`
- Score: UNIX timestamp (float or int)
- Member: `username`

### Task Requirements

1. **Implement the `/audit` Endpoint:**
   Modify `/home/user/audit_api/app.py` to handle GET requests at `/audit?username=<username>&resource=<resource_name>`.
   
2. **Graph Projection & Schema Analysis:**
   Using a single SQL query (preferably a Recursive CTE), determine all roles the user has. This includes roles directly assigned in `user_roles` AND all inherited roles (if Role A is a parent of Role B, and the user has Role B, they also possess the permissions of Role A).
   Check if *any* of these resolved roles possess the permission for the requested `resource_name` via `role_permissions`.

3. **Result Sorting & Cross-Query Aggregation:**
   Query Redis to find the **top 3 most recent** access timestamps for this specific user on the requested resource.

4. **Output Format:**
   The endpoint must return a JSON response with exactly this structure and key naming:
   ```json
   {
     "username": "jdoe",
     "resource_name": "financial_records",
     "authorized": true,
     "granted_by_roles": ["admin", "finance_viewer"], 
     "recent_access_timestamps": [1690000000.0, 1680000000.0, 1670000000.0]
   }
   ```
   - `authorized`: Boolean. `true` if any of their resolved roles have the permission, otherwise `false`.
   - `granted_by_roles`: A list of strings containing the `role_name`s that granted access to this resource. Must be **alphabetically sorted**. If `authorized` is false, this should be an empty list `[]`.
   - `recent_access_timestamps`: A list of the 3 most recent timestamp scores from Redis for this user/resource, sorted in descending order (most recent first). If fewer than 3 exist, return what is available.

5. **Service Integration:**
   Start your Flask application on port 8080. You can use Gunicorn or the built-in Flask dev server, as long as it listens on `0.0.0.0:8080`.

Ensure your queries are optimized. The compliance verifier will aggressively test this endpoint with various combinations of users and resources.