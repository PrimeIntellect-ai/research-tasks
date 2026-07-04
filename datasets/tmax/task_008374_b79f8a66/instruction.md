You are an operations engineer triaging a critical incident in our daily data processing pipeline. 

The pipeline consists of a primary Bash script located at `/home/user/pipeline.sh`. It reads log lines from a file, enriches the data by querying a local SQLite database (`/home/user/data/enrichment.db`), and writes the output to a file. 

Currently, when we run the pipeline on today's logs (`/home/user/data/logs.txt`), it crashes unexpectedly with a non-zero exit code. The script works fine on yesterday's logs.

Your tasks are to:
1. **Delta Debugging:** The `logs.txt` file contains thousands of lines. You must write a script to minimize the input and isolate the exact single line in `logs.txt` that is causing the pipeline to crash. Save this exact single log line to `/home/user/failing_line.txt`.
2. **Intermediate State & Query Debugging:** Trace the execution of `/home/user/pipeline.sh` to determine why this specific line causes a crash. The script relies on a SQLite query that is failing.
3. **Fix the Pipeline:** Modify `/home/user/pipeline.sh` so that it handles this edge case gracefully without crashing. The fix must be implemented strictly in Bash (e.g., properly escaping variables or sanitizing input before the query). If the query succeeds, it should output the role; if the user doesn't exist, it should default to "UNKNOWN". 
4. **Final Execution:** Once fixed, run `/home/user/pipeline.sh /home/user/data/logs.txt`. The script should complete successfully (exit code 0) and generate `/home/user/output.log`.

Requirements for verification:
- `/home/user/failing_line.txt` must contain exactly the one line from `logs.txt` that triggers the crash.
- `/home/user/pipeline.sh` must be patched to run without errors on the provided `logs.txt`.
- `/home/user/output.log` must be fully generated containing all enriched log lines.

All operations must be performed as the `user` user. You have access to standard Linux utilities, `sqlite3`, and `bash`.