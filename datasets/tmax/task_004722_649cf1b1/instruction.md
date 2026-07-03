You are a Database Reliability Engineer managing a massive, custom backup storage system. 

We have an SQLite database at `/home/user/backups.sqlite` containing metadata for over 250,000 backup chunks across thousands of servers. 

Our legacy retention policy engine is compiled as a standalone binary located at `/app/retention_oracle`. It determines whether a specific backup chunk is obsolete and can be safely deleted. You can run it manually by providing metadata parameters, like so:
`/app/retention_oracle <chunk_id> <server_id> <file_path_hash> <timestamp> <chunk_size> <is_encrypted>`
It outputs exactly `1` (obsolete, delete it) or `0` (keep it).

However, `/app/retention_oracle` is a stripped binary with artificial delays and significant overhead. Calling it 250,000 times in a shell loop or Python subprocess will take hours, which is unacceptable for our daily cron job.

Your task:
1. Analyze the schema of `/home/user/backups.sqlite` (which includes tables for servers, files, and chunks).
2. Reverse-engineer or deduce the logic inside `/app/retention_oracle` by treating it as a black box (fuzzing/sampling it) or by inspecting the binary. The logic relies on advanced windowing concepts (e.g., how many newer backups exist for the same file, cumulative sizes, etc.).
3. Write a highly optimized Python script `/home/user/generate_cleanup.py` that connects to the SQLite database and uses native SQL window functions, aggregations, and filtering to exactly replicate the oracle's logic.
4. Your script must process the entire database in under 5 seconds and output a file at `/home/user/obsolete_chunks.csv`.
5. The CSV must contain a single column `chunk_id` (with a header row) listing every chunk that the oracle *would* have flagged as `1`.

We will evaluate your generated `obsolete_chunks.csv` against a hidden ground-truth list using an F1-score metric. To pass, your implementation must achieve an F1-score of exactly 1.0 (perfect precision and recall) and run in the allotted time.