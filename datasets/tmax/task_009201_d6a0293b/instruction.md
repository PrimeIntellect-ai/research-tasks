As a compliance officer, I need to audit our system's access controls to ensure no unauthorized users have access pathways to databases containing Personally Identifiable Information (PII). 

I have extracted two files that represent our system's access graph:
1. `/home/user/inventory.json`: A JSON array containing all nodes in our system. Each node has an `id`, a `type` (User, Server, or Database), and type-specific attributes. Users have an `authorized` boolean (true if they are cleared for PII). Databases have a `contains_pii` boolean.
2. `/home/user/access_edges.csv`: A CSV file with headers `source,target` representing directed access rights (e.g., User -> Server, or Server -> Database).

Your task is to write and execute a Python script (`/home/user/audit.py`) that performs the following graph projection and pattern matching:
1. Build a directed graph from the provided inventory and edges.
2. Identify all "Database" nodes where `contains_pii` is `true`.
3. Identify all "User" nodes where `authorized` is `false`.
4. Determine which unauthorized users have a directed path (of any length) to one or more PII databases.
5. Aggregate the findings and export them to `/home/user/violations.json`.

The output `/home/user/violations.json` must exactly match this schema:
```json
{
  "violations": [
    {
      "user": "<user_id>",
      "reachable_pii_dbs": ["<db_id>", "<db_id>"]
    }
  ]
}
```
Constraints for the output:
- Only include unauthorized users who can actually reach at least one PII database.
- The `violations` list must be sorted alphabetically by the `user` string.
- The `reachable_pii_dbs` list for each user must be sorted alphabetically.
- Format the JSON with an indentation of 2 spaces.

You may install any Python packages you need (like `networkx`) locally.