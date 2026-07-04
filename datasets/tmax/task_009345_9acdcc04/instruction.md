You are a Database Reliability Engineer (DBRE) investigating a repository of NoSQL database backup chunks. The metadata for these chunks was exported from our NoSQL catalog into a JSON Lines format, but the data model documentation was lost. 

We know the following:
- The data is located at `/home/user/backup_metadata.jsonl`.
- Each line is a JSON document representing a backup chunk.
- There are two types of backups: `"full"` and `"incremental"`.
- Incremental backups are linked to other backups, forming a dependency tree (a hierarchical chain) that ultimately roots at a `"full"` backup. You will need to reverse-engineer the exact field names used for relationships and sizes by inspecting the JSON data.

Your task is to write and execute a Go program (`/home/user/analyze_chains.go`) that performs the equivalent of a recursive NoSQL aggregation pipeline to calculate the total storage footprint of each complete backup chain. 

A "backup chain" consists of a single root `"full"` backup and all of its recursive `"incremental"` descendants. 

Your Go program must output the summarized results to a CSV file located at `/home/user/chain_summary.csv` with the following requirements:
1. The CSV must have exactly three columns in this order: `root_id,total_size_mb,chunk_count`
2. `root_id` is the identifier of the `"full"` backup at the root of the chain.
3. `total_size_mb` is the sum of the sizes of all chunks in the chain (including the root).
4. `chunk_count` is the total number of chunks in the chain.
5. The rows must be sorted by `total_size_mb` in descending order. If sizes are tied, sort by `root_id` alphabetically.
6. The file must include a header row.

Write the code, execute it to generate the CSV, and ensure the final file is formatted correctly.