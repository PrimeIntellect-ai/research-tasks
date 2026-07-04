You have inherited an unfamiliar data processing codebase located at `/home/user/repo`. The core program, `process_data`, is written in C and is responsible for deserializing binary sensor streams and calculating moving averages. 

Recently, the data pipeline has started experiencing statistical anomalies and convergence failures, resulting in crashes. You need to investigate this regression.

Please perform the following debugging steps:
1. **Regression Finding:** Use `git` to find the exact commit that introduced the bug. The program is built using `make`. You can test if a commit is "good" or "bad" by running `make clean && make && ./process_data`. A successful run returns an exit code of `0`. The bug causes the program to fail with a non-zero exit code. The initial commit in the repository is known to be good, and the current `HEAD` is bad.
2. **Memory Dump Analysis:** A previous crash generated a raw memory dump file located at `/home/user/crash.dmp`. The program throws a specific serialization encoding error before it crashes, which remains in the memory dump. Extract this error code. The error code always starts with the prefix `FATAL_ENC_ERR_` followed by an alphanumeric sequence.

Once you have identified the culprit commit and extracted the error code, create a report file at `/home/user/report.txt` with exactly two lines:
- Line 1: The full git commit hash of the first bad commit.
- Line 2: The exact error code string extracted from the dump.