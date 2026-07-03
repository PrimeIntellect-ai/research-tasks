You are tasked with investigating a memory leak in a long-running Python worker service. The team has reported that the service randomly runs out of memory under heavy concurrent load, but the issue is intermittent and hard to reproduce locally.

Here is what we know:
1. The code is located in a local Git repository at `/home/user/service-repo`.
2. There is a load-testing script `load_test.py` in the repository that can reliably trigger intermittent concurrency issues and memory leaks. However, running it requires a valid `TEST_AUTH_TOKEN` environment variable.
3. The original developer accidentally committed this token to the repository in the past, but later removed it from the code and the current history. You will need to use Git forensics to recover this deleted secret token so you can run the test suite.
4. Once you can run the test suite, you need to identify *when* the memory leak was introduced. The bug was introduced sometime in the past 30 commits. Identify the exact commit that introduced the memory leak.
5. Identify the root cause of the race condition/memory leak in `worker.py` and fix it on the `main` branch. 

When you have completed your investigation and fixed the bug, create a file named `/home/user/report.txt` with exactly three lines:
- Line 1: The recovered secret token.
- Line 2: The full, complete commit hash (40 characters) of the commit that originally introduced the memory leak.
- Line 3: The exact name of the Python function in `worker.py` where you fixed the race condition/memory leak.

The automated test will verify the contents of `/home/user/report.txt` and ensure that `python load_test.py` now passes without any memory leak detected.