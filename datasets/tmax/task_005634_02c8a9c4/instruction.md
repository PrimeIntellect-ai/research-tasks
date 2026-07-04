You are an IT support technician. We've received a high-priority ticket from the analytics team regarding a custom log aggregation script.

**Ticket Details:**
The script `/home/user/log_aggregator.py` is supposed to read all `.log` files in `/home/user/logs/` concurrently and count the occurrences of different log levels (`ERROR`, `WARN`, `INFO`). However, the total counts in the output file (`/home/user/summary.json`) are often inconsistent and lower than they should be, suggesting a race condition during concurrent execution.

Your task is to reproduce, trace, and fix the issue.

**Instructions:**
1. **Fuzz Testing:** Write a python script named `/home/user/fuzzer.py` to generate test data. It must create 50 log files in `/home/user/logs/` (e.g., `log_1.log` to `log_50.log`). Each file must contain exactly 1,000 lines. Each line should be formatted as `LEVEL|Some random message`, where `LEVEL` is randomly chosen from `ERROR`, `WARN`, or `INFO`.
2. **Intermediate Tracing & Fix:** Investigate `/home/user/log_aggregator.py`. You will notice a race condition in how the global `event_counts` dictionary is updated. Fix the concurrency bug using proper thread synchronization (e.g., `threading.Lock`).
3. **Validation:** Run your fixed script. The total sum of all values in the generated `/home/user/summary.json` must reliably equal exactly 50,000 across multiple runs. 
4. **Resolution:** Create a file `/home/user/ticket_resolution.txt` containing only the final exact count of `ERROR` logs as reported by your fixed script's `summary.json`.

**Constraints:**
- Do not change the overall threading architecture of `log_aggregator.py` (it must still process each file in a separate thread).
- Do not use external libraries, only standard Python modules.