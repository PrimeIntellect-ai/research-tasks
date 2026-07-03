You are a data analyst working with a proprietary graph database engine. 

In `/home/user/data/`, there are two large CSV files:
- `nodes.csv` (columns: `node_id`, `type`, `status`, `region`)
- `edges.csv` (columns: `source_id`, `target_id`, `relationship_type`, `weight`)

There is a compiled query engine at `/app/graph_engine`. It is a stripped binary that processes these CSVs using a NoSQL-style JSON aggregation pipeline. 

You have been given a working, but extremely slow, pipeline at `/home/user/naive_pipeline.json`. This pipeline identifies a critical vulnerability pattern: "Server" nodes in "us-east" that depend on "Database" nodes with an "offline" status. 

The `naive_pipeline.json` currently performs expensive `$lookup` (graph traversal/join) operations on the entire dataset *before* applying `$match` filters, causing it to evaluate millions of intermediate paths. 

Your task:
1. Analyze the structure of `/home/user/naive_pipeline.json` to understand the custom NoSQL syntax accepted by `/app/graph_engine`.
2. Apply query optimization principles (e.g., predicate pushdown) to rewrite the pipeline. You must filter the nodes as early as possible before the joins (`$lookup`).
3. Save your highly optimized pipeline to `/home/user/optimized_pipeline.json`.

You can test your pipeline by running:
`/app/graph_engine --nodes /home/user/data/nodes.csv --edges /home/user/data/edges.csv --pipeline /home/user/optimized_pipeline.json --out /home/user/results.json`

Requirements:
- Your `optimized_pipeline.json` MUST produce the exact same output array in `results.json` as the `naive_pipeline.json`.
- The execution time of your optimized pipeline must be significantly faster (at least 5x speedup).
- You may use Python to analyze the data or generate the JSON if helpful, but the final deliverable is the `/home/user/optimized_pipeline.json` file.