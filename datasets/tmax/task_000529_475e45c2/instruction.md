You are a DevOps engineer responsible for maintaining a log processing pipeline. Recently, our new job dependency tracking script, `/home/user/log_processor.py`, has been hanging indefinitely in production when processing certain large log files, forcing us to restart the service. The script parses job state transitions and resolves dependency trees.

Your task is to debug the system and implement a robust fix. You must:

1. **Find the Root Cause & Create an MRE**: Analyze `/home/user/log_processor.py` and the provided log file `/home/user/production_logs.txt`. Use tracing or fuzz testing to isolate the exact minimal sequence of log lines that causes the script to hang. 
2. Save this minimal reproducible example to `/home/user/mre_log.txt`. This file should contain *only* the absolute minimum number of log lines required to trigger the infinite loop.
3. **Fix the Bug**: Modify `/home/user/log_processor.py` to prevent the hang. If the invalid state that causes the hang is encountered, the `resolve_dependencies` function should immediately raise a `ValueError` with the exact message `"Cycle detected in job dependencies"` rather than getting stuck.
4. **Write a Regression Test**: Create a Python script at `/home/user/regression_test.py` that imports `log_processor` and calls `log_processor.process_logs()` with the contents of `/home/user/mre_log.txt`. 
   - The test script must catch the `ValueError` and exit with code `0` to indicate the fix works. 
   - If the script hangs, it should timeout and exit with code `1`. 
   - If it completes without raising the expected error, it should exit with code `2`.

Do not change the function signature of `process_logs(log_lines)`.