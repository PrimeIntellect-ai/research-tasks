You are a DevOps engineer tasked with debugging a critical issue in our log aggregation pipeline. 

Our dashboards are suddenly reporting massive spikes in 5xx errors at strange hours, and it's throwing off our daily SLA calculations. We suspect a timezone-related bug was recently introduced into our custom log parsing package, which processes Nginx-style logs and aggregates errors by the hour.

The log parsing utility is a vendored package located at `/app/bash-log-metrics/`. It is a Git repository. 
Currently, the `HEAD` of the `main` branch produces incorrect aggregations for the provided production logs. We know for a fact that the tag `v1.0.1` was working perfectly and produced the correct UTC-based hourly buckets.

Your objectives:
1. **Regression Finding:** Use `git bisect` (or a similar technique) within the `/app/bash-log-metrics/` repository to identify the exact commit that introduced the timezone bug. The bug causes the hourly error buckets to shift or group incorrectly.
2. **Root Cause Analysis:** Inspect the traceback, debug the bash script execution, and analyze the diff of the bad commit to understand what went wrong.
3. **Implementation & Fix:** Fix the bug in the current `HEAD` of the `main` branch (do not just checkout the old tag; apply the fix to the latest code so we keep other recent features).
4. **Data Transformation:** Once fixed, run the tool on our production log file located at `/home/user/prod_access.log`.
   The tool is executed as:
   `bash /app/bash-log-metrics/bin/aggregate.sh /home/user/prod_access.log`
5. **Output Verification:** Save the stdout of the fixed script to exactly `/home/user/hourly_errors.csv`.

The output format is a CSV with two columns: `Hour,ErrorCount` (e.g., `2023-10-15 16:00,42`). 

Our automated verifier will calculate the Mean Squared Error (MSE) between your `/home/user/hourly_errors.csv` and the known ground-truth metrics. To pass, your output must be highly accurate.