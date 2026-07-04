You are a database reliability engineer handling graph database backups. We recently exported a subgraph of our critical service dependencies using a Cypher query, resulting in two CSV files: `/home/user/nodes.csv` and `/home/user/edges.csv`. 

Our external auditing tool does not support graph formats or Cypher. It requires a NoSQL document representation (JSON) of this dependency graph.

Your task is to write a C program named `/home/user/map_backup.c` that reads the two CSV files and converts this graph representation into a hierarchical JSON document at `/home/user/backup.json`.

The input files have the following structures:
`/home/user/nodes.csv`:
```csv
id,type,name
```

`/home/user/edges.csv`:
```csv
source_id,target_id,relationship
```

The output `/home/user/backup.json` must strictly follow this JSON schema structure:
```json
{
  "services": [
    {
      "id": "<node_id>",
      "dependencies": ["<target_id_1>", "<target_id_2>"]
    }
  ]
}
```

**Requirements:**
1. Only include nodes of type `Service` in the output.
2. The `dependencies` array should contain the `target_id`s of all outgoing edges from the source node where the relationship is `DEPENDS_ON`.
3. The `services` array must be sorted alphabetically by the `id` field.
4. The `dependencies` array for each service must also be sorted alphabetically.
5. If a service has no dependencies, output an empty array `[]`.
6. Compile your C program to `/home/user/map_backup` using `gcc` and run it to produce `/home/user/backup.json`. Ensure the output is valid JSON (you can test your output using `jq`).

The CSV files already exist on the system.