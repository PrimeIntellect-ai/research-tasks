You are an operations engineer triaging a critical incident. We deploy a background task processing script located at `/home/user/app/worker.py`. Recently, we have noticed data inconsistencies indicating that records are being dropped under high concurrent load.

The code is version-controlled in a local Git repository at `/home/user/app`. 
We know the application worked perfectly at the commit tagged `v1.0`. The current `main` branch (HEAD) is broken.

Your task:
1. Identify and fix a local environment misconfiguration that currently causes `worker.py` to crash immediately upon startup (masking the actual concurrency issue). The script requires a specific environment variable to run, which is currently missing in your shell. You can inspect `worker.py` to find out what it expects. The file path it looks for does not need to exist, but the environment variable must be set.
2. Construct a minimal reproducible regression test script at `/home/user/test_bisect.py`. This script should:
   - Setup the correct environment variables for the worker.
   - Initialize a file named `counter.txt` in `/home/user/app` with the value `0`.
   - Execute `/home/user/app/worker.py 50` (spawning 50 threads, each doing 100 operations).
   - Read the final value from `counter.txt`.
   - Exit with code `0` if the value is exactly `5000` (success/thread-safe), and exit with code `1` if the value is anything else (failure/race condition).
3. Use `git bisect` in conjunction with your `test_bisect.py` script to find the exact commit that introduced the race condition.
4. Once you have identified the first bad commit, save its full 40-character SHA hash to `/home/user/bad_commit.txt`.

Constraints:
- All operations must be performed within the `/home/user/app` directory.
- Use Python to write the regression test.
- Do not modify the history of the Git repository.