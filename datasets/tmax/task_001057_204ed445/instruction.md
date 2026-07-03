You are a support engineer tasked with debugging and fixing a broken diagnostic collection pipeline. The pipeline is designed to parse multiple log files concurrently, trace error chains within those logs, and output a consolidated JSON report. However, it currently fails due to a combination of shell scripting errors, algorithmic bugs, and concurrency issues.

The pipeline is located at `/home/user/diagnostics/` and consists of two main files:
1. `/home/user/diagnostics/run_pipeline.sh`: A bash script that finds all `.log` files in `/home/user/logs/` and launches a Python processor for each one in the background to process them concurrently.
2. `/home/user/diagnostics/parse_trace.py`: A Python script that reads a log file, recursively traces the root cause of an error using the references inside the log, and appends the result to `/home/user/diagnostics/report.json`.

Currently, the pipeline has three major issues you need to fix:
1. **Filename Handling**: `run_pipeline.sh` breaks when processing log files that contain spaces in their filenames. You must fix the bash script so it correctly handles filenames with spaces while still launching the Python processors concurrently.
2. **Infinite Recursion**: `parse_trace.py` contains a recursive function `find_root_cause` that follows "Caused by" references in the log file. Some logs contain circular error references (e.g., Error A caused Error B, which caused Error A). This causes the script to crash with a `RecursionError`. Fix the algorithm to detect and break out of circular references (return the ID of the last unique error found before the cycle).
3. **Race Condition**: `parse_trace.py` reads, updates, and writes to the shared `/home/user/diagnostics/report.json` file. Because `run_pipeline.sh` spawns these Python scripts concurrently, a race condition occurs, resulting in corrupted JSON or missing entries. Fix the Python script so that concurrent executions safely write to the JSON file without losing data or corrupting the format (e.g., using file locking).

After fixing these issues, you must construct a regression test:
Create a bash script at `/home/user/test_pipeline.sh`. This script should:
1. Clear any existing `/home/user/diagnostics/report.json`.
2. Run `/home/user/diagnostics/run_pipeline.sh` and wait for all background jobs to finish.
3. Programmatically verify that `/home/user/diagnostics/report.json` is a valid JSON array.
4. Programmatically verify that the JSON array contains exactly 5 entries (since there are 5 log files).
5. Exit with status `0` if all checks pass, and `1` if any check fails.

Make sure your regression test is executable (`chmod +x /home/user/test_pipeline.sh`). You can test your fixes by running your regression test script.