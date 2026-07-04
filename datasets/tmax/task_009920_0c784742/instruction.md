As a compliance officer, I need your help auditing our system's access control graph to ensure that only authorized personnel have access to sensitive customer data.

We have an export of our identity and access management (IAM) graph exported as a JSON-Lines file located at `/home/user/graph_data.jsonl`. 

Each line in the file is a JSON object representing either a `Node` or an `Edge`.
Nodes have the following schema:
`{"type": "node", "id": "string", "label": "User|Role|Resource", "name": "string"}`

Edges have the following schema:
`{"type": "edge", "from": "string", "to": "string", "relation": "HAS_ROLE|INHERITS|CAN_ACCESS"}`

The access model works as follows:
1. A `User` is assigned to a `Role` via a `HAS_ROLE` edge (from User to Role).
2. A `Role` can inherit permissions from another `Role` via an `INHERITS` edge (from child Role to parent Role). This inheritance can be deeply nested (recursive).
3. A `Role` is granted access to a `Resource` via a `CAN_ACCESS` edge (from Role to Resource).
4. A `User` has access to a `Resource` if there is a valid path from the User to the Resource following `HAS_ROLE`, zero or more `INHERITS`, and a final `CAN_ACCESS` edge.

Your task is to write a Go program at `/home/user/audit.go` that parses this file, builds the knowledge graph, and finds all `User` nodes that have access (either directly or through inherited roles) to the `Resource` node named `"customer_pii_db"`.

Your Go program must output the results to `/home/user/flagged_users.txt`. 
The output file must contain the ID and Name of each user with access, one per line, sorted alphabetically by the user's `id`, in the following exact format:
`id,name`

For example:
`u1,Alice`
`u4,David`

You can use standard Go libraries. Compile and run your script to generate the output file.