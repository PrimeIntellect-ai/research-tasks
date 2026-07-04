You are acting as a Database Reliability Engineer. Our system has recently migrated its backup metadata catalog to a multi-service architecture running locally on this machine. There is a MongoDB instance storing backup metadata and a mocked internal object storage service holding the raw logs. 

Currently, the services are defined and started via a script located at `/app/start_services.sh`, which brings up:
1. A MongoDB instance on `127.0.0.1:27017` (contains the `backups` database with `jobs` and `chunks` collections).
2. A lightweight local HTTP server on `127.0.0.1:8080` (serves raw validation logs).

Your task is to write a highly optimized Rust CLI tool in `/home/user/backup_analyzer` that queries this NoSQL database, processes the results, and exports a validated summary report.

Specifically, you need to:
1. Reverse engineer the data model by inspecting the `jobs` and `chunks` collections in MongoDB. 
2. Write a Rust program (using `mongodb` and `tokio` crates) that performs a NoSQL aggregation pipeline to:
   - Filter jobs where the `status` is "COMPLETED" and `retention_days` > 30.
   - Join (using `$lookup`) the `chunks` collection to calculate the total backup size per job.
   - Sort the results by `completion_time` descending.
   - Paginate the results to fetch only the top 500 largest valid backups by size.
3. Export these 500 records to `/home/user/report.jsonl`.
4. Validate the output: each line in `report.jsonl` must strictly adhere to this JSON schema: `{"job_id": "string", "total_size_bytes": "number", "completion_date": "string (ISO8601)", "is_archived": "boolean"}`. The `is_archived` flag should be computed as `true` if `retention_days` > 365, otherwise `false`.

**Performance Requirement:**
The previous implementation took over 15 seconds to pull and process 50,000 records. Your Rust implementation must execute the aggregation pipeline efficiently on the database side rather than in-memory. The verifier will run your compiled Rust binary (`/home/user/backup_analyzer/target/release/backup_analyzer`), and the entire execution must take **less than 1.5 seconds** to produce the correct `report.jsonl`.

Please create the Rust project, implement the solution, compile it in release mode, and ensure `/home/user/report.jsonl` is generated correctly and within the time threshold.