You are a Database Reliability Engineer (DBRE) tasked with managing and verifying database backups. We have a system that dumps backup job metadata into JSON files, but the system is flaky and sometimes produces malformed logs or records failed jobs. 

Your task is to write a robust Bash pipeline/script to process these results, validate them, construct a valid backup restoration graph, and calculate analytical aggregations.

Setup:
The backup metadata logs are stored in the directory `/home/user/backup_logs/`. Each file is a JSON document representing a single backup job.

Write a Bash script at `/home/user/analyze_backups.sh` that performs the following steps when executed:

1. **Output Schema Validation**: Read all JSON files in `/home/user/backup_logs/`. A valid backup log MUST contain the following top-level keys: `job_id`, `cluster`, `type` (either "full" or "incremental"), `parent_job_id` (can be null for full backups), `status`, `size_bytes` (integer), and `timestamp` (integer). Discard any logs that are missing one or more of these keys, or if the JSON is malformed.

2. **Query-to-pipeline chaining**: Filter the valid logs to include ONLY those where `status` is `"success"` and `cluster` is `"db-cluster-omega"`.

3. **Graph projection and materialization**: Out of the successful jobs for `db-cluster-omega`, you need to project a "restoration chain". A restoration chain must start with a `full` backup. Subsequent `incremental` backups must link to the previous backup in the chain via their `parent_job_id` (i.e., `parent_job_id` of job N must equal the `job_id` of job N-1). Find the longest valid continuous chain of successful backups. If there is a tie in length, pick the chain whose final incremental backup has the largest `size_bytes`.

4. **Analytical aggregation**: For the selected longest restoration chain, compute the cumulative backup size (running total of `size_bytes`) at each step.

5. **Output**: Your script must output the result to a CSV file located at `/home/user/restore_chain.csv`. The CSV must have the following header:
   `job_id,type,cumulative_size_bytes`
   Each subsequent row should represent a job in the selected restoration chain, ordered from the `full` backup to the final `incremental` backup.

Constraints:
- Use standard shell built-ins, coreutils, and standard CLI tools like `jq`, `awk`, `grep`, `sort`, etc.
- Your script should not require root privileges or installing arbitrary packages (assume standard tools are available).
- Run your script once before finishing to ensure `/home/user/restore_chain.csv` is generated.