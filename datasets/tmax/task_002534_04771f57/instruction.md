You are a Database Reliability Engineer. Our backup management system recently experienced a failure, and the automated pipeline generated a recording of the monitoring dashboard at `/app/backup_run.mp4`. Concurrently, the metadata for these backup operations—represented as a directed acyclic graph (DAG)—is stored in a SQLite database at `/home/user/backups.db`.

Our preliminary query to find impacted downstream dependencies is timing out due to an implicit cross join that creates a Cartesian product of all graph nodes. 

Your task:
1. **Video Analysis:** Extract frames from `/app/backup_run.mp4` using `ffmpeg`. Identify the exact timestamp (in whole seconds) of any frame containing the text "CORRUPT" (you can use `tesseract` for OCR). These seconds correspond to the `job_id`s of the failed backups.
2. **Graph Pattern Matching & Query Optimization:** Write a corrected SQL query (avoiding the cross join) to find all downstream backup jobs in `/home/user/backups.db` that depend on these corrupted `job_id`s. The database has two tables: `nodes` (`job_id`, `status`) and `edges` (`source_id`, `target_id`).
3. **Multi-Protocol Service:** Create a Bash-based HTTP API using `nc` (netcat) or `socat`. The service must listen on `127.0.0.1:9090`. 
4. **Output Schema:** When the verifier makes an HTTP GET request to `/impacted_backups`, your Bash server must respond with a standard HTTP 200 OK headers followed by a JSON payload precisely matching this schema:
`{"corrupted_jobs": [id1, id2], "impacted_downstream_jobs": [id3, id4, id5]}`

Ensure your Bash HTTP server remains running in the background so the automated test can verify it. Write your optimized SQLite query to `/home/user/optimized_graph.sql`.