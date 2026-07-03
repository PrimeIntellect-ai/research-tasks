You are an AI assistant helping a backup administrator process historical backup logs. 

We have a backup archive located at `/home/user/backups.tar.gz`. It contains multiple log files with multi-line records. You need to write a C program to parse these logs, filter them based on a configuration file, and safely write the matching results to a single output file. Because we want to process logs concurrently in bash, your C program must use file locking.

Here are your instructions:

1. **Extract and Verify**: Extract `/home/user/backups.tar.gz` into `/home/user/logs/`.
2. **Configuration**: You have a configuration file at `/home/user/filter.conf` containing the following format:
   ```
   TARGET_STATUS=FAILED
   MIN_FILES=10
   ```
3. **C Program (`/home/user/parser.c`)**: 
   Write a C program that takes three arguments: `<log_file> <config_file> <output_json_file>`.
   - It should first parse `<config_file>` to get the `TARGET_STATUS` and `MIN_FILES`.
   - It should then parse `<log_file>` which contains multi-line records like:
     ```
     BEGIN_JOB
     JobID: 105
     Status: FAILED
     Files: 15
     END_JOB
     ```
   - For every record that matches BOTH the `TARGET_STATUS` and has `Files` >= `MIN_FILES`, append it as a single-line JSON string to `<output_json_file>`. 
     Format: `{"JobID": 105, "Status": "FAILED", "Files": 15}`
   - **Crucial**: Use `fcntl` or `flock` to acquire an exclusive lock on the output file before appending the JSON line, and release it afterward. This is required because we will run instances in parallel.
4. **Execution**:
   Compile your C program to `/home/user/parser`.
   Run the parser concurrently for all `.log` files in the extracted `/home/user/logs/` directory using bash job control (`&` and `wait`). Store the output in `/home/user/failed_jobs.json`.

Ensure `/home/user/failed_jobs.json` is perfectly formatted with one JSON object per line. Do not print anything to the output file other than the matching JSON lines.