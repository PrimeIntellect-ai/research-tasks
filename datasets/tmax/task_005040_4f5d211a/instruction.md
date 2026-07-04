You are a Database Reliability Engineer (DBRE) tasked with building a tool to extract and map backup dependency metadata. Our automated backup orchestrator uses a local undocumented SQLite database to store backup jobs and their prerequisite dependencies. 

We need to export these dependency graphs into a Document format (JSON) so they can be ingested by our new NoSQL reporting dashboard. 

Your objective is to write a C program that connects to this database, reverse-engineers its schema, and extracts the full dependency tree for a given backup job using parameterized queries.

Requirements:
1. The SQLite database is located at `/home/user/backup_mgr.db`. You will need to inspect it to determine the exact table and column names representing the backup jobs and their directed dependencies (a graph structure where one job depends on another).
2. Write a C program at `/home/user/export_graph.c` and compile it to `/home/user/export_graph`.
3. The program must take exactly one command-line argument: the name of the root backup job to query (e.g., `./export_graph "app_server_backup"`).
4. The C code **must** use prepared statements with parameterized queries (e.g., `sqlite3_bind_int`, `sqlite3_bind_text`) to traverse the graph and prevent SQL injection.
5. The program should recursively (or iteratively) traverse all dependencies for the provided job and map this relational/graph data into a nested JSON document.
6. The output must be written to a file named `/home/user/dependency_doc.json`.

JSON Output Format Specification:
The output must be a valid JSON object matching this structure exactly:
```json
{
  "job": "app_server_backup",
  "dependencies": [
    {
      "job": "db_cluster_1",
      "dependencies": [
        {
          "job": "network_storage_A",
          "dependencies": []
        }
      ]
    },
    {
      "job": "auth_service",
      "dependencies": [
        {
          "job": "network_storage_A",
          "dependencies": []
        }
      ]
    }
  ]
}
```
*Note: The order of elements in the `dependencies` array does not matter, but the nested relationships must be correct based on the database graph.*

Before you consider the task complete, ensure you run `./export_graph "app_server_backup"` to generate the final `/home/user/dependency_doc.json` file.