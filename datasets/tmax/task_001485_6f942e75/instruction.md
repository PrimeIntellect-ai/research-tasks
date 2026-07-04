You are a performance engineer investigating a severe bottleneck in a data processing pipeline. The pipeline processes mathematical sequences (specifically, calculating Collatz conjecture sequence lengths for large integers) but a recent batch caused the pipeline workers to stall indefinitely.

Your environment is set up in `/home/user/`.
You have the following resources:
1. **Container Logs:** `/home/user/logs/pipeline.log` contains recent logs from the processing containers.
2. **Workload Database:** `/home/user/db/workload.db` is an SQLite3 database containing the raw input data. It has a table named `measurements` with columns `batch_id` (INTEGER) and `input_value` (INTEGER).
3. **Profiler Script:** `/home/user/bin/collatz_profiler.sh` is a copy of the Bash script used by the workers to process a list of numbers. It takes a single file as an argument (where each line is an integer) and processes them sequentially.

Your task is to:
1. **Log Inspection:** Analyze `/home/user/logs/pipeline.log` to identify the `batch_id` that caused the worker to stall/timeout. Save this exact batch ID to a file named `/home/user/failed_batch.txt`.
2. **Query Debugging:** Extract all `input_value`s for that specific `batch_id` from the SQLite database and save them, one per line, to `/home/user/extracted_inputs.txt`.
3. **Delta Debugging / Minimization:** The `collatz_profiler.sh` script hangs indefinitely when run on `extracted_inputs.txt` due to a mathematical edge case (an integer overflow bug in Bash arithmetic causing an infinite loop). You must write a delta debugging script or use a minimization strategy (using Bash) to isolate the **single** minimal `input_value` from `extracted_inputs.txt` that triggers this infinite loop. 
4. **Result:** Once isolated, save this single integer to `/home/user/minimal_bug.txt`.

*Note: You may consider a run "hung" or "stalled" if `collatz_profiler.sh` takes more than 2 seconds to process a single number or a small set of numbers.*

Ensure that:
- `/home/user/failed_batch.txt` contains only the numeric batch ID.
- `/home/user/minimal_bug.txt` contains only the single integer causing the failure.