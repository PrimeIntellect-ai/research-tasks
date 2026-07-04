You are a performance engineer tasked with debugging a critical data processing pipeline written entirely in Bash. 

Recently, the data engineering team noticed three major issues in the production pipeline:
1. Some records are being processed multiple times due to a concurrency bug (race condition).
2. The pipeline occasionally stalls, indicating a severe performance bottleneck.
3. The logs from the different containerized worker nodes are scattered and need to be correlated.

The system state has been captured and exported to your environment. You will find three log files from the worker nodes in `/home/user/logs/`:
- `worker_A.log`
- `worker_B.log`
- `worker_C.log`

Each log entry is formatted as: `[TIMESTAMP] [PID] [ACTION] [RECORD_ID] [DURATION_MS]`

Your task is to analyze these logs, identify the bugs, and write a fixed processing script.

**Step 1: Log Timeline & Error Diagnosis**
Inspect the logs in `/home/user/logs/` and reconstruct the timeline. You need to identify:
- Which worker process (give the PID) successfully processed the highest number of records overall?
- There is a race condition where a specific Record ID was picked up and processed by multiple workers simultaneously. Which Record ID was duplicated?
- One specific Record ID caused a massive performance bottleneck, taking significantly longer to process than any other record. Which Record ID was it?

Output your findings to a new file `/home/user/analysis.txt` with exactly three lines:
Line 1: The PID of the worker that processed the most records.
Line 2: The Record ID that was duplicated.
Line 3: The Record ID that caused the performance bottleneck.

**Step 2: Concurrency & Performance Fix**
The original buggy script logic used by the workers was essentially this:
```bash
#!/bin/bash
# buggy_worker.sh
FILE="/home/user/data/queue.txt"
while [ -s "$FILE" ]; do
    RECORD=$(head -n 1 "$FILE")
    sed -i '1d' "$FILE"
    # ... processing logic ...
    echo "$RECORD processed" >> /home/user/data/completed.txt
done
```
This logic causes race conditions when multiple workers run concurrently. 

Write a new, fixed Bash script at `/home/user/fixed_worker.sh` that:
1. Reads from `/home/user/data/queue.txt`.
2. Uses standard Bash tools (like `flock`) to safely read and remove lines one by one, preventing race conditions even if 5 instances of `/home/user/fixed_worker.sh` are run simultaneously in the background.
3. Appends the processed record string (e.g., `REQ-XXXX processed`) to `/home/user/data/completed.txt`.
4. Is executable (`chmod +x`).

To test your script, we will place 100 new records into `/home/user/data/queue.txt` and launch 5 background instances of your `fixed_worker.sh` script simultaneously. Your script must ensure exactly 100 lines are written to `completed.txt` without any duplicates or dropped records.