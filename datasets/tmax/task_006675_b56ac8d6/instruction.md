You are a site reliability engineer investigating a memory leak in a long-running Python log processing service. The service is located at `/home/user/log_processor.py` and processes an input log file containing JSON lines.

Recently, the service has been crashing with Out-Of-Memory (OOM) errors when processing large logs. We suspect that intermittent corrupted input lines are causing the service to cache failed requests indefinitely, leading to a memory leak.

You have been provided with a sample log file at `/home/user/requests.log` which reproduces the issue.

Your task is to:
1. Debug `/home/user/log_processor.py` to identify the root cause of the memory leak. Fix the code so that it handles corrupted inputs gracefully without unbounded memory growth (e.g., remove the caching of failed requests in global lists, or handle the exception without leaking).
2. Use test minimization or debugging techniques to identify the exact corrupted lines in `/home/user/requests.log` that were triggering the intermittent failures and the leak.
3. Write the 1-indexed line numbers of these corrupted lines to `/home/user/corrupted_lines.txt`. Ensure the line numbers are sorted in ascending order, with one number per line.
4. Run your fixed `/home/user/log_processor.py` on `/home/user/requests.log`. The script outputs a total sum of valid request values. Save this numeric output to `/home/user/final_total.txt`.

Make sure to leave the fixed `/home/user/log_processor.py` in place.