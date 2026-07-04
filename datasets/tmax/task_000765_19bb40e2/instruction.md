You are a data engineer building a diagnostic ETL pipeline. We have a diagnostic tool that encodes database transaction lock requests and grants into a video format (for a legacy monitoring dashboard). We need to extract this data and detect deadlocks.

First, analyze the video provided at `/app/transaction_monitor.mp4`. The video consists of frames where the average brightness of the top-left 10x10 pixels encodes a transaction ID, and the top-right 10x10 pixels encodes a resource ID. A lock request is represented by a frame; if a resource is already locked by another transaction, it creates a wait-for dependency.

Step 1: Write a Bash script `extract_logs.sh` that uses `ffmpeg` to parse `/app/transaction_monitor.mp4` and outputs a CSV file `transactions.csv` with columns: `timestamp,transaction_id,resource_id`.

Step 2: Write a Bash script `detect_deadlocks.sh` that takes a CSV file (in the format of `transactions.csv`) as its first argument and outputs all transaction IDs that are involved in a deadlock (a cycle in the wait-for graph). The output should be a comma-separated list of transaction IDs on a single line, sorted numerically, for each cycle detected, one cycle per line. 

Your `detect_deadlocks.sh` must be robust as it will be fuzzed with various generated CSV files to ensure bit-exact equivalence with our reference cycle-detection oracle. It must rely only on standard Bash built-ins, coreutils, and `awk`.

Ensure both scripts are executable.