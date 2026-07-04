Hello, I am escalating an issue from our tier 1 support. Our distributed calculation worker crashed overnight. 

You need to perform a diagnostic and recovery task:

1. **Analyze and Fix**: The script `/home/user/worker.py` failed with a `RecursionError` during execution. Analyze the script. The `calculate_weight` function is missing a base case for values less than or equal to 0. Update `/home/user/worker.py` so that if `n <= 0`, it returns `0`.
2. **Resume Operations**: Once fixed, run the test script `python /home/user/run_system.py` to process the remaining queued tasks. This will generate new logs.
3. **Reconstruct Timeline**: We need a chronological timeline of all events to understand the state before and after the crash. There are log files in `/home/user/logs/` (some from before the crash, some from after). Extract all lines containing "TASK_EVENT" from all `.log` files in that directory.
4. **Generate Report**: Sort these extracted lines strictly chronologically by their timestamp. Output the sorted lines into a new file at `/home/user/diagnostic_report.txt`. 

The format of `/home/user/diagnostic_report.txt` must be exactly the raw extracted "TASK_EVENT" log lines, sorted by time, one per line.