You are a performance engineer tasked with debugging a critical bash-based log processing pipeline that has recently experienced a severe performance regression. 

The repository is located at `/home/user/log_processor`. The main script, `process_logs.sh`, processes a large log file and extracts warnings and errors. 
Historically, this script processed our standard 20,000-line test file (`/home/user/large_logs.txt`) in a fraction of a second. However, on the current `main` branch (`HEAD`), it takes significantly longer, causing downstream timeouts.

We know that the commit tagged `v1.0` is fast and correct. The current `main` branch produces the correct output but is unacceptably slow.

Your tasks are:
1. **Automated Bisection**: Write a test harness script to validate the intermediate state of the program. This script must assert two things: 
   - The output of `bash process_logs.sh /home/user/large_logs.txt` exactly matches the expected correct output (which you can generate using the `v1.0` version).
   - The execution time is under 1.5 seconds.
   Use this test harness with `git bisect run` to find the exact commit that introduced the performance regression.

2. **Root Cause Analysis & Fix**: Analyze the faulty commit to understand why the performance degraded. Once identified, checkout the `main` branch and fix `process_logs.sh` so that it maintains the added features/logic of `main` (if any, though in this case you just need to ensure correct log extraction) but runs efficiently (under 1.5 seconds) and produces the correct output. Commit your fix to the `main` branch.

3. **Reporting**: Create a file at `/home/user/regression_report.txt` with exactly the following format:
```
Bad Commit: <full_40_char_hash_of_the_commit_that_introduced_the_slowness>
Status: fixed
```

Note: 
- Do not modify `/home/user/large_logs.txt`.
- Your final `process_logs.sh` on `main` must output the exact same text as the `v1.0` version when run against `/home/user/large_logs.txt`.