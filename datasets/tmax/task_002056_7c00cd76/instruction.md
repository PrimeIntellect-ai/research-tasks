You are a forensics engineer investigating a severe memory leak in a long-running simulation service. The service recently crashed with an Out of Memory (OOM) error. Your goal is to reconstruct the timeline from distributed logs, diagnose a subtle numerical instability causing the memory leak, create a minimal reproducible example, and apply a fix.

**Environment:**
*   `/home/user/logs/api.log` - Contains API gateway logs with request payloads.
*   `/home/user/logs/worker.log` - Contains the background worker logs and system resource alerts.
*   `/home/user/app/processor.py` - The core logic running the simulation.
*   `/home/user/app/test_suite.py` - A test suite to verify the service works normally (must pass after your fix).

**Your Tasks:**
1.  **Log Timeline Reconstruction:** Correlate the timestamps between `api.log` and `worker.log` to identify the specific `request_id` and the parameters (`start_val`, `lr`) that triggered the memory spike and crash.
2.  **MRE Creation:** Create a minimal reproducible example at `/home/user/mre.py`. This script must import `compute_trajectory` from `app.processor`, call it with the exact parameters that caused the crash, and exit. 
3.  **Error Diagnosis & Fix:** The memory leak is caused by a numerical instability in `processor.py` that bypasses the normal convergence checks, causing the system to continuously allocate memory up to a failsafe limit. Modify `/home/user/app/processor.py` to correctly detect if the value has diverged to infinity or NaN (`math.isinf`, `math.isnan`) and break the loop immediately, returning the history up to that point.
4.  **Reporting:** Create a file at `/home/user/report.txt` with exactly two lines:
    *   Line 1: The `request_id` that caused the crash.
    *   Line 2: The `lr` (learning rate) value from that request.

**Verification Requirements:**
*   `python3 /home/user/app/test_suite.py` must print "OK".
*   `/home/user/report.txt` must contain the correct extracted data.
*   `/home/user/mre.py` must run and finish in under 1 second after your fix.