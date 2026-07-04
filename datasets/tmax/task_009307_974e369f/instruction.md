You are a Database Reliability Engineer (DBRE) responsible for ensuring the integrity of your company's infrastructure metadata backups. The metadata is exported daily from a graph database into flat CSV files. 

Before committing the latest backup to cold storage, you need to audit the raw backup files to detect structural anomalies (dangling edges) and identify critical security compliance violations (databases missing backup storage configurations) by matching a specific knowledge graph pattern.

You have been provided with two backup files:
1. `/home/user/backup_data/nodes.csv` (Columns: `id`, `label`, `name`)
2. `/home/user/backup_data/edges.csv` (Columns: `src`, `dst`, `rel`)

Write a Bash script at `/home/user/audit_graph.sh` that leverages `sqlite3` to analyze these CSV files and perform the following tasks:

1. **Find Dangling Edges:** Identify any edges where either the `src` or `dst` node ID does not exist in `nodes.csv`. Save these exactly as they appear in the original CSV (format: `src,dst,rel`) to `/home/user/dangling_edges.csv`.

2. **Knowledge Graph Pattern Matching & Materialization:** Find all "vulnerable" databases. A database is vulnerable if it matches this specific sub-graph pattern:
   An `Engineer` (node label) -[`MANAGES`]-> a `Cluster` (node label) -[`HOSTS`]-> a `Database` (node label) 
   **AND** that `Database` does NOT have a `HAS_BACKUP` relationship to any node.
   
   You must use complex joins and subqueries to project this graph pattern and materialize the results into `/home/user/vulnerable_dbs.csv`. 
   The output must be a headerless CSV with the format: `engineer_name,cluster_name,database_name`.
   Sort the output alphabetically by `engineer_name`, then `cluster_name`, then `database_name`.

Requirements:
- Your script `/home/user/audit_graph.sh` must be executable (`chmod +x`).
- Your script should quietly perform the operations without requiring interactive prompts.
- You must use `sqlite3` within your Bash script to load the data into memory, execute the complex graph queries, and export the results.

Please create the bash script and execute it to generate the required output files.