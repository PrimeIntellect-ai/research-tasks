You are a Database Reliability Engineer (DBRE) responsible for validating graph database backups of our backup infrastructure. The backup consists of two files: `/home/user/nodes.json` and `/home/user/edges.json`. 

These files represent a knowledge graph of our systems, containing nodes with labels `Database`, `BackupJob`, and `StorageNode`, and edges with types `HAS_BACKUP` and `STORED_ON`.

Your task is to write a Go program `/home/user/analyze_backup.go` that reads these files and performs the following operations:

1. **Output Schema Validation**: Validate the schema of all `BackupJob` nodes. Every `BackupJob` node must have both a `status` (string) and a `timestamp` (string, valid ISO8601 format) in its `properties`. Your program must find all `BackupJob` nodes that fail this validation and write their `id`s as a JSON array of strings to `/home/user/schema_errors.json`.

2. **Knowledge Graph Pattern Matching**: Find all `Database` nodes that are connected to a `BackupJob` (via a `HAS_BACKUP` edge) where the `BackupJob` has `status` equal to `"FAILED"`, and that `BackupJob` is connected to a `StorageNode` (via a `STORED_ON` edge) where the `StorageNode` has `type` equal to `"S3"`. Your program must extract the `name` property of these `Database` nodes and write them as a JSON array of strings to `/home/user/failed_s3_dbs.json`.

3. **Index Strategy Design**: To optimize the query plan for finding failed backup jobs, we need to add an index. Write the exact Cypher query required to create a b-tree index on the `status` property of the `BackupJob` label. Save this exactly as a single line in `/home/user/index_strategy.txt`.

Ensure your Go program is self-contained and uses standard libraries. Run your Go program so the output files are generated.