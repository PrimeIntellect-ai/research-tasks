You are an on-call engineer who just received a 3 AM page. An internal data aggregation service has started crashing periodically after a recent deployment, leaving behind a custom memory dump and failing on a specific batch of payloads. The service works on most data but fails on certain edge cases due to an integer handling bug introduced recently. 

You need to investigate this issue using the files located in `/home/user/service`. 

Perform the following debugging steps and record your findings:

1. **Memory Dump Analysis**:
   The crashed process left a partial memory dump at `/home/user/service/core.dump`. Find the last processed user ID before the crash. The ID is stored in memory as a string formatted like `LAST_USER_ID=U<numbers>`. Extract just the user ID (e.g., `U123456`) and write it to `/home/user/solution_userid.txt`.

2. **Git Bisection**:
   The service code is in a local Git repository at `/home/user/service`. There is a test script `/home/user/service/test_runner.py` that you can run against the provided `payload_large.dat` file. The test script exits with code 0 if successful, and 1 if the bug is present.
   Use `git bisect` (or any other method) to find the exact commit hash that introduced the bug. Write the full 40-character commit hash to `/home/user/solution_commit.txt`.

3. **Delta Debugging / Payload Minimization**:
   The file `/home/user/service/payload_large.dat` contains 100 payload records (one per line). Most of them are valid, but at least one triggers the integer overflow/unpacking bug in the bad commit. Isolate the *single line* from `payload_large.dat` that triggers the crash when passed to `test_runner.py`. Write that exact single line to `/home/user/solution_minimized_payload.txt`.

Ensure your final solution files are formatted exactly as requested, containing only the requested data (no extra text or newlines if possible).