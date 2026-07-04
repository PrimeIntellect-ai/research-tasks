You are assisting a compliance officer who is auditing our internal systems. We need to determine exactly which users have access to a highly sensitive document, `DOC-77X`, by tracing nested group memberships.

You are provided with two data sources:
1. A SQLite database at `/home/user/iam.db` containing our Identity and Access Management (IAM) data.
   - Table `users`: `id` (INTEGER PRIMARY KEY), `username` (TEXT)
   - Table `groups`: `id` (INTEGER PRIMARY KEY), `group_name` (TEXT)
   - Table `group_members`: `group_id` (INTEGER), `member_user_id` (INTEGER NULL), `member_group_id` (INTEGER NULL). 
     *Note: A group can contain users directly, or it can contain other groups (nested groups). If `member_user_id` is NOT NULL, a user is in the group. If `member_group_id` is NOT NULL, a group is in the group.*

2. A JSON document at `/home/user/policies.json` containing our document access policies. It maps document IDs to a list of group names that are granted access.

Your task:
Write and execute a Python script at `/home/user/audit.py` that performs the following:
1. Reads `/home/user/policies.json` to find which groups have direct access to `DOC-77X`.
2. Queries `/home/user/iam.db` to recursively resolve all users who belong to those groups, either directly or indirectly through nested group memberships. You may use recursive CTEs in SQLite or recursion in Python.
3. Outputs the final list of authorized usernames for `DOC-77X` to a JSON file at `/home/user/audit_result.json`.

The output file `/home/user/audit_result.json` must strictly conform to this JSON schema:
```json
{
  "document": "DOC-77X",
  "authorized_users": ["list", "of", "usernames", "sorted", "alphabetically"]
}
```

Ensure the users array is alphabetically sorted and contains no duplicates.