You are an engineer investigating a severe memory leak in a long-running log processing service. 

We have extracted a memory snapshot from the container and saved it to `/home/user/service_dump.bin`. The service uses a Python parsing script located at `/home/user/parser.py`. The parser attempts to extract usernames from log lines matching the format `USER_LOGIN: <username>;`, but there is an edge case in the format parsing that causes unfinished log entries to be buffered indefinitely in memory.

Your task is to:
1. **Analyze the memory dump:** Extract strings from `/home/user/service_dump.bin` to find the exact username that is heavily repeated and causing the memory leak (it's the one missing the expected termination character).
2. **Document the culprit:** Write *only* the exact leaked username (no prefixes, no spaces) to a new file at `/home/user/leaked_username.txt`.
3. **Fix the edge-case:** Modify `/home/user/parser.py`. Change the behavior of the `process_log(log_line)` function so that if a `USER_LOGIN:` line is missing the terminating `;`, it immediately raises a `ValueError("Missing semicolon")` instead of appending the username to the `leaked_records` list. Ensure it still correctly parses valid lines.
4. **Construct a regression test:** Create a test script at `/home/user/test_parser.py` that imports `process_log` from `parser.py`. Write a test that passes a log line containing the malformed, leaked username you discovered, and asserts that a `ValueError` is correctly raised. The script should exit with code 0 if the test passes.

Provide the commands you use to analyze the dump, apply the fix, and write the test.