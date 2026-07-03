You are an automation specialist tasked with building a lightweight data processing pipeline in Bash. We need to extract structured security events from a raw server log, orchestrate the steps with a basic DAG (Directed Acyclic Graph) approach, and monitor the pipeline's execution.

Your task is to create and execute a Bash script at `/home/user/run_dag.sh` that processes a raw log file located at `/home/user/raw_logs/server.log`. 

The pipeline must consist of three logical steps executed in order, where subsequent steps only run if the previous step succeeds (returns exit code 0). 

**Step 1: EXTRACT**
- Read `/home/user/raw_logs/server.log`.
- Find all lines corresponding to failed SSH password attempts. These lines contain the phrase "Failed password".
- Save these raw lines to `/home/user/failed_attempts.txt`.

**Step 2: TRANSFORM**
- Read `/home/user/failed_attempts.txt`.
- Parse each line to extract three pieces of information:
  1. The timestamp (e.g., "Jan 15 10:15:22")
  2. The username attempted (e.g., "admin" or "root". Note: sometimes the log says "invalid user admin", in which case the user is "admin").
  3. The IP address (e.g., "192.168.1.50")
- Format this extracted data into a single, valid JSON array of objects and save it to `/home/user/structured_data.json`.
- The JSON objects must have the exact keys: `"timestamp"`, `"user"`, and `"ip"`.

**Pipeline Logging (MONITOR)**
- As your script runs, it must log the execution status of each step to `/home/user/pipeline.log`.
- The format for each line in the log must be exactly: `[YYYY-MM-DD HH:MM:SS] [STEP_NAME] [STATUS]`
- Valid step names are `EXTRACT` and `TRANSFORM`.
- Valid statuses are `SUCCESS` or `FAILED`.
- Example log entry: `[2023-10-27 15:04:02] EXTRACT SUCCESS`

**Requirements:**
1. Create the Bash script at `/home/user/run_dag.sh`.
2. Make it executable and run it to produce `/home/user/structured_data.json` and `/home/user/pipeline.log`.
3. You may use standard Unix text processing utilities (awk, sed, grep, jq, etc.). Do not use Python or other high-level languages.