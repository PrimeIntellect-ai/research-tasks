You are a Database Reliability Engineer investigating a legacy backup system. The backup dependency metadata is stored in a SQLite database, but the retrieval process is severely bottlenecked, and the tool used to derive backup encryption keys has been stripped of its source code.

Your objective is to optimize the database, reconstruct the backup dependency graph, perform graph analytics to find the most critical backup jobs, and expose a microservice that provides the decryption keys for these critical jobs.

Step 1: Database Optimization
You have a SQLite database at `/home/user/backups.db` containing two tables:
- `jobs` (id TEXT PRIMARY KEY, type TEXT)
- `deps` (source TEXT, target TEXT)

The current query used to materialize the dependency graph is:
`SELECT j1.id, j2.id FROM jobs j1 JOIN deps d ON j1.id = d.source JOIN jobs j2 ON d.target = j2.id WHERE j1.type = 'incremental' AND j2.type = 'full';`

This query is currently too slow. Use `EXPLAIN QUERY PLAN` to understand the bottleneck. Create the necessary indexes in `/home/user/backups.db` to optimize this query so it executes efficiently.

Step 2: Graph Projection and Analytics
Using Python, extract the edges returned by the optimized query. Build a directed graph where an edge goes from `source` to `target`. 
Using the `networkx` library, compute the PageRank of all nodes in this graph (use the default `alpha=0.85` and `max_iter=100`). 
Identify the top 5 nodes with the highest PageRank scores. These are the most critical "full" backup jobs that multiple incremental backups rely on.

Step 3: Key Derivation
A legacy, stripped compiled binary is located at `/app/key_deriver`. We do not have the source code. You can run it by passing a backup job ID as an argument:
`/app/key_deriver <job_id>`
It will output the decryption key for that job to stdout. 

Step 4: Microservice Deployment
Create and start a Python HTTP server listening on `0.0.0.0:8000`. 
It must implement a single `GET` endpoint at `/critical_keys`.
When accessed, this endpoint must return a JSON object mapping the top 5 critical backup job IDs to their derived decryption keys. 

Example response:
```json
{
  "job_999": "a1b2c3d4...",
  "job_123": "f5e6d7c8...",
  ...
}
```

Ensure the server remains running in the background or foreground so that the automated verifier can query it.