You are acting as an automated compliance auditor. We are conducting an access review of our internal systems, specifically focusing on the `SWIFT_PAYMENT_GATEWAY` resource. 

Our access control data is stored in an SQLite database located at `/home/user/rbac.db`. The database implements a Role-Based Access Control (RBAC) system with role hierarchies (a directed acyclic graph where roles can inherit permissions from other roles).

The database has the following schema:
- `users` (id INTEGER PRIMARY KEY, username TEXT, created_at DATETIME)
- `roles` (id INTEGER PRIMARY KEY, role_name TEXT)
- `role_hierarchy` (parent_role_id INTEGER, child_role_id INTEGER) -- 'parent_role_id' inherits all permissions from 'child_role_id'
- `user_roles` (user_id INTEGER, role_id INTEGER)
- `role_permissions` (role_id INTEGER, resource_name TEXT)

Your task is to write a Python script `/home/user/audit.py` that connects to this database and performs the following:
1. Uses a **Recursive Common Table Expression (CTE)** to traverse the role hierarchy graph and find ALL roles that have access to the `SWIFT_PAYMENT_GATEWAY` resource (both directly via `role_permissions` and indirectly via inheritance in `role_hierarchy`).
2. Joins these roles with the `users` table to find all users who possess these roles. If a user has multiple paths to the permission, return the role closest to the user (or just any valid role they hold that grants the access). For simplicity, you can just map the user to the role they are directly assigned that ultimately grants this access.
3. Uses an SQL **Window Function** to assign an `audit_rank` to each user, ordered by their `created_at` timestamp descending (most recently created user gets rank 1).
4. Exports the results to `/home/user/audit_report.json`.

The output JSON must strictly adhere to this schema (list of objects):
```json
[
  {
    "audit_rank": 1,
    "username": "user1",
    "assigned_role": "role_name"
  }
]
```

Run your script so that `/home/user/audit_report.json` is generated. Ensure that your script handles the graph traversal strictly within the SQLite query.