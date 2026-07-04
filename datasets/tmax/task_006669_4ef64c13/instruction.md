You are acting as a Database Reliability Engineer. We are auditing our backup infrastructure. 

We have a backup dependency graph stored in a SQLite database located at `/home/user/backup_graph.db`. This database uses a generic graph schema (which you will need to reverse-engineer) to store our infrastructure components and their relationships.

A junior engineer wrote a Go tool located at `/home/user/extract_chain.go` to find specific knowledge graph patterns: the chain of dependencies from a specific `Service` to its `Database` and finally to its underlying `Storage`. 

Unfortunately, the tool is broken. The SQL query inside it is returning millions of incorrect rows because of an implicit cross-join (Cartesian product) missing its proper edge relationship constraints. Furthermore, it doesn't properly parameterize the target service name, making it unsafe and hard to reuse.

Your task is to:
1. Reverse engineer the schema of `/home/user/backup_graph.db` to understand how nodes and edges are mapped.
2. Fix the Go code in `/home/user/extract_chain.go`. The tool should accept exactly one command-line argument: the name of the Service (which is stored in a JSON property inside the node).
3. The SQL query must be rewritten to correctly traverse the graph pattern `Service -> Database -> Storage` using explicit JOINs (or correctly constrained WHERE clauses) on the edge table, and it MUST use a parameterized query for the Service name input.
4. The Go program must output the results to `/home/user/dependency_chains.json` as a strictly formatted JSON array of objects. 

The output JSON schema must look exactly like this:
```json
[
  {
    "service_name": "<name of the service>",
    "database_name": "<name of the database>",
    "storage_name": "<name of the storage>"
  }
]
```
(Note: the names should be extracted from the `name` key within the `props` JSON column of the respective nodes).

Initialize the Go module in `/home/user/` (name it `backup-audit`), fetch the necessary SQLite driver (`github.com/mattn/go-sqlite3`), build the executable, and run it for the service named `"PaymentService"`.

Ensure the resulting `/home/user/dependency_chains.json` contains only the valid dependency chains for "PaymentService" without any cross-join duplicates.