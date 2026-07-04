You are a Database Reliability Engineer (DBRE) responsible for auditing our database backup infrastructure. We recently exported our infrastructure knowledge graph into CSV files, and we need to verify that all critical databases have adequate backup policies.

We will use KùzuDB (an in-process property graph database) via its Rust API to perform this analysis. 

Your task is to write a Rust tool that loads the infrastructure graph, identifies vulnerable databases using Cypher pattern matching, outputs the query plan for optimization auditing, and validates the output schema before saving it.

Requirements:
1. Initialize a new Rust project named `backup_auditor` at `/home/user/backup_auditor`. Add the `kuzu` crate and `serde_json` crate.
2. The infrastructure graph data is located in `/home/user/graph_data/` (you can assume the files are already there):
   - `databases.csv` (Columns: id, name, critical)
   - `policies.csv` (Columns: id, retention_days, active)
   - `has_policy.csv` (Columns: from_db_id, to_policy_id)
3. Your Rust program must:
   - Create an embedded Kùzu database in `/home/user/kuzu_db`.
   - Define the schema using Cypher:
     - Node table `Database` (id STRING, name STRING, critical BOOLEAN, PRIMARY KEY (id))
     - Node table `BackupPolicy` (id STRING, retention_days INT64, active BOOLEAN, PRIMARY KEY (id))
     - Rel table `HAS_POLICY` (FROM Database TO BackupPolicy)
   - Import the data from the CSV files into these tables using Kùzu's `COPY` command.
4. Write a Cypher query to find the `id` of all `Database` nodes that are `critical = true` but DO NOT have a `HAS_POLICY` relationship to a `BackupPolicy` where `active = true` AND `retention_days >= 30`.
5. Execute an `EXPLAIN` on this exact query and write the resulting query plan (the raw string returned by Kùzu) to `/home/user/query_plan.txt`.
6. Execute the actual query to get the vulnerable database IDs.
7. Format the output as a JSON array of strings (e.g., `["db_id_1", "db_id_2"]`). Order the IDs alphabetically.
8. Validate the JSON array. It must strictly be a JSON array of string literals. If valid, save this JSON array to `/home/user/vulnerable_dbs.json`.

Run your Rust program so that both `/home/user/query_plan.txt` and `/home/user/vulnerable_dbs.json` are generated successfully.