You are acting as a compliance officer auditing system access rights. 

We have an export of our identity and access management system in a CSV file located at `/home/user/edges.csv`. This file represents a graph of access rights with three columns: `source,target,type`. The `type` can be `HAS_ROLE`, `IN_GROUP`, or `CAN_ACCESS`.

The previous auditor tried to write a shell script to find all resources a user can access by using sequential `join` commands. Unfortunately, their approach resulted in implicit cross joins and infinite loops because our group hierarchy contains cycles (e.g., `GroupA` is in `GroupB`, and `GroupB` is in `GroupA`).

Your task is to write a pure Bash script (standard Linux CLI tools like `awk`, `grep`, `sed`, `sort`, etc. are allowed) located at `/home/user/audit.sh` that takes a single user ID as an argument and performs a proper graph traversal to find all distinct resources that the user can ultimately access.

A user can access a resource if there is a path from the user to the resource using any combination of `HAS_ROLE` and `IN_GROUP` edges, ending with a `CAN_ACCESS` edge to a resource.

Your script must:
1. Accept a user ID as the first argument (e.g., `./audit.sh u_charlie`).
2. Traverse the graph recursively/hierarchically, handling any cyclic relationships without infinite loops.
3. Identify all target nodes that are reached via a `CAN_ACCESS` edge.
4. Output the final accessible resources to `stdout` in the following strict JSON schema, sorted alphabetically by the resource name:

```json
[
  {"user": "<USER_ID>", "resource": "<RESOURCE_1>"},
  {"user": "<USER_ID>", "resource": "<RESOURCE_2>"}
]
```
(Be precise with spacing and format: two spaces for indentation, one space after colons, double quotes for keys and values, brackets on their own lines).

After writing the script, execute it for the user `u_charlie` and redirect the output to `/home/user/charlie_access.json`.