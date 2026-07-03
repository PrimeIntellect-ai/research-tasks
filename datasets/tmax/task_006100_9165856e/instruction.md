As a compliance officer auditing our internal financial systems, I need to identify Separation of Duties (SoD) violations. We recently exported our access control matrix into a set of flat CSV files, but the role hierarchy makes it difficult to see what permissions a user actually holds.

Your task is to write a Go program that analyzes these schemas, materializes the role hierarchy graph, projects all inherited permissions to the users, and exports a compliance report of any users who have a "Toxic Combination" of permissions.

The exported data is located in `/home/user/audit_data/` and consists of:
1. `users.csv` - Columns: `user_id, user_name`
2. `roles.csv` - Columns: `role_id, role_name`
3. `user_roles.csv` - Columns: `user_id, role_id` (Direct roles assigned to a user)
4. `role_hierarchy.csv` - Columns: `parent_role_id, child_role_id` (The `parent_role_id` inherits all permissions of the `child_role_id`. This inheritance is transitive, meaning if A inherits B, and B inherits C, then A inherits C.)
5. `role_permissions.csv` - Columns: `role_id, permission_name` (Direct permissions assigned to a role)

The specific Separation of Duties (SoD) violation we are auditing is the combination of `FUNDS_INITIATE` and `FUNDS_APPROVE`. No single user should have both permissions, either directly or through role inheritance.

Write a Go program at `/home/user/audit.go`. When executed, it must:
1. Parse the CSV files.
2. Build a graph to map the role hierarchy and project inherited permissions.
3. Determine the full set of permissions for each user.
4. Identify any users possessing BOTH `FUNDS_INITIATE` and `FUNDS_APPROVE`.
5. Export the results to exactly `/home/user/sod_violations.json`.

The output JSON file must be a JSON array of objects, sorted by `user_id` in ascending order. Each object must strictly match this format:
```json
[
  {
    "user_id": "U001",
    "user_name": "Alice Smith",
    "violation": true
  }
]
```
Do not include users who do not have a violation.