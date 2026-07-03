You are a compliance officer auditing an enterprise access-control system. You need to accomplish two distinct tasks related to our authorization pipeline.

**Part 1: Fix the Vendored Authorization Parser**
Our legacy C-based authorization loader uses a vendored version of `cJSON` (version 1.7.15) located at `/app/vendor/cJSON`. Recently, a bad patch was applied that causes graph data models to parse incorrectly. Specifically, object key lookups are returning null, which leads to implicit cross-joins in our downstream SQL database ingestion because foreign keys are dropped.
Your task is to:
1. Locate the bug in `/app/vendor/cJSON/cJSON.c` that breaks case-sensitive object item retrieval.
2. Fix the bug.
3. Build the library using `make` and install it so that the shared object updates the system's `/usr/local/lib/libcjson.so`.

**Part 2: Implement the Audit Query Tool**
You must write a standalone program (in any language) located at `/home/user/audit_query`. This program must strictly replicate the behavior of our verified oracle `/opt/oracle/audit_oracle`.

Your program will be invoked exactly like this:
`/home/user/audit_query <path_to_graph_db.json> <user_id>`

The `graph_db.json` is a NoSQL document containing:
- `users`: Array of objects with `id` (string), `clearance` (integer), and `roles` (array of strings).
- `roles`: Array of objects with `id` (string), `inherits` (array of strings - recursive role IDs), and `categories` (array of strings).
- `resources`: Array of objects with `id` (string), `category` (string), and `classification` (integer).

**Access Rules:**
A user has access to a resource if AND ONLY IF:
1. The user has a role (either directly or recursively inherited) that grants access to the resource's `category`.
2. The user's `clearance` is GREATER THAN OR EQUAL TO the resource's `classification`.

**Output Format:**
Your program must output a single line to `stdout` containing a comma-separated, alphabetically sorted list of `resource_id`s the user can access.
Example output: `res_alpha,res_delta,res_omega`

*Note:* Beware of implicit cross-joins when evaluating multiple paths to the same role. A user might inherit the same category multiple times, but resources should only be listed once.

Ensure your script is executable (`chmod +x /home/user/audit_query`). If you write it in an interpreted language, use the appropriate shebang (e.g., `#!/usr/bin/env python3`).