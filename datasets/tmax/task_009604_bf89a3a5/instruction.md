You are a Database Administrator tasked with optimizing a graph traversal query in an SQLite database. 

We have an SQLite database located at `/home/user/hierarchy.db` with a single table:
`nodes (id INTEGER PRIMARY KEY, parent_id INTEGER)`

Currently, recursive queries used to traverse the graph are suffering from poor performance because full table scans are occurring when looking up child nodes. 

Your tasks are:
1. Identify the missing index that would optimize queries looking up children by their parent. Create this index on the `nodes` table and name it exactly `idx_parent_id`.
2. Write a recursive query (using a Common Table Expression) to find all descendant nodes of the node with `id = 7`. Do not include node 7 itself in the descendants list.
3. Export the query results to a JSON file located at `/home/user/output.json`.
4. Ensure the output strictly follows this JSON schema:
```json
{
  "target_node": 7,
  "descendants": [ /* array of descendant IDs sorted in ascending order */ ]
}
```

You may use shell tools like `sqlite3`, `jq`, or write a short script in the language of your choice. Ensure the exact file paths and names are used.