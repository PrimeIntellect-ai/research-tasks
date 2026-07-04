You are a Database Reliability Engineer investigating a corrupted Identity and Access Management (IAM) backup. 

A recent backup of the IAM graph was saved as an SQLite database at `/home/user/backup.db`. Due to an application-level bug, the system started writing soft-deleted edges as active, but a previous DBRE identified the issue and added a `deleted` column to the `edges` table. However, the existing indexes are completely fragmented and causing full table scans for graph projections.

Your task involves database index optimization, graph projection, and NoSQL materialization.

**Step 1: Index Strategy**
The database contains two tables:
- `nodes` (`id` INTEGER PRIMARY KEY, `type` TEXT, `name` TEXT)
- `edges` (`id` INTEGER PRIMARY KEY, `source` INTEGER, `target` INTEGER, `rel_type` TEXT, `deleted` INTEGER)

To optimize graph extraction, you must create a covering index on the `edges` table named `idx_edges_extract`. This index must optimize queries that filter by `rel_type` and `deleted`, while covering the `source` and `target` columns. 
- Create this index in the database.
- Save the exact `CREATE INDEX` SQL DDL statement you used to a file at `/home/user/index.sql`.

**Step 2: Graph Analytics & Materialization**
Extract the graph and materialize it into a NoSQL document format (JSON Lines).
Only consider:
- Nodes of type `user` (as source) and `group` (as target).
- Edges with `rel_type = 'member_of'` where `deleted = 0`.

For every user that is a member of at least one active group, calculate their out-degree centrality (the total number of active groups they belong to). Output the results to `/home/user/users_graph.jsonl`. 

Each line in the file must be a valid JSON object matching this exact schema:
`{"username": "<user_name>", "centrality": <count>, "groups": ["<group_name_1>", "<group_name_2>"]}`

**Constraints for the JSONL file:**
- The `groups` array must be sorted alphabetically for each user.
- The lines in the JSONL file must be sorted alphabetically by the `username`.
- Do not include users who have a centrality of 0.

You may use standard Linux tools (like `sqlite3`, `jq`, `awk`, etc.) or write shell/SQL scripts to accomplish this.