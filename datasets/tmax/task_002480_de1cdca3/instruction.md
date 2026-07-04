You are an on-call engineer who just received a 3 AM PagerDuty alert. The nightly log aggregation pipeline has failed. 

The pipeline runs a Python script located at `/home/user/process_logs.py` to parse access logs stored in the `/home/user/logs/` directory. The script is suddenly crashing with a `ValueError`, halting the entire pipeline. 

Your tasks are:
1. **Isolate the Fault (Delta Debugging):** The log files contain thousands of lines. You must isolate the *exact single log line* that causes the script to crash. Once you find it, save this exact single line to `/home/user/buggy_line.txt`.
2. **Fix the Script:** Modify `/home/user/process_logs.py` so that it handles the problematic log entry gracefully without crashing. The script should be able to process all log files in `/home/user/logs/` and exit with a `0` status code. You don't need to extract accurate analytics from the malformed line—just ensure the script skips it or handles it without raising an unhandled exception.

Do not delete or modify the original log files in `/home/user/logs/`.