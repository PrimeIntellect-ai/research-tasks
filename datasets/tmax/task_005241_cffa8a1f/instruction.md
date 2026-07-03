You are tasked with debugging and bisecting a regression in a Rust log parsing application. 
The repository is located at `/home/user/log_parser_repo`.

Recently, an intermittent assertion failure was introduced: `Total log entries parsed incorrectly! Race condition detected.` 
The application spawns multiple threads to process a log file (`test.log`), counting occurrences of different log levels. Because the bug is a race condition, it does not happen on every single run. You may need to run the compiled binary multiple times to reliably reproduce the failure.

The repository contains 200 commits. The initial commits are known to be working perfectly, but a regression was introduced somewhere in the middle of the history.

Your tasks are:
1. Identify the exact commit that introduced the regression. Use `git bisect` combined with a script that runs the program enough times to catch the intermittent race condition.
2. Once you find the first bad commit, write its full 40-character commit hash to `/home/user/bad_commit_hash.txt`.
3. Identify the root cause of the race condition in the current `HEAD` commit. Fix the bug, and save your corrected version of the source code to `/home/user/fixed_parser.rs`. Your fixed code must compile and reliably pass the assertions without race conditions.

Constraints:
- Do not modify the `test.log` file.
- The fixed parser should still use threading and process the data concurrently.