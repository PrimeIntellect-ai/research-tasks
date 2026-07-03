You are a DevOps engineer debugging a log processing pipeline that has started failing. 

We have a script `/home/user/process_logs.py` that processes a large log file located at `/home/user/server.log`. The script is currently failing, but the exact cause and the specific offending log line are unknown.

Your task is to fix the environment, isolate the faulty data, patch the script, and write a regression test. 

Perform the following steps:
1. **Environment Misconfiguration Repair**: `process_logs.py` immediately crashes upon execution with a runtime error before even touching the logs. Fix the environment variable misconfiguration required by the script so it can run.
2. **Delta Debugging / Minimization**: Once the script runs, it will crash with a `JSONDecodeError` while processing `/home/user/server.log`. The log file contains 1,000 lines. Write a temporary delta-debugging or bisection script to find the *single* exact line causing the crash. Write this exact line (as plain text) to a new file named `/home/user/bad_log_line.txt`.
3. **Patch the Script**: Modify `/home/user/process_logs.py`. In the `process_line` function, catch the `json.JSONDecodeError` and instead raise a custom `LogFormatError` (the exception class is already defined in the file) with the exact message `"Invalid log format"`.
4. **Regression Test Construction**: Create a regression test file at `/home/user/test_regression.py` using the standard `unittest` framework. It must import `process_line` and `LogFormatError` from `process_logs`. Write a test case `test_corrupt_log_line` that asserts `process_line` raises `LogFormatError` when passed the exact string content of the bad line you found in step 2.

Ensure your regression test passes when run via `python3 -m unittest /home/user/test_regression.py`.