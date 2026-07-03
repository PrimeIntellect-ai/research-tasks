You are tasked with debugging a regression in a Go service that processes incoming jobs. Recently, a bug was introduced that causes goroutines to leak when the service handles corrupted input and the context is cancelled. 

There is a git repository located at `/home/user/repo`. The repository contains 50 commits. Somewhere along the line, the goroutine leak was introduced.

We have a bisection test script at `/home/user/repo/test.sh` that runs the test suite. However, it is currently failing to run because of an environment misconfiguration.

Additionally, we pulled a raw goroutine dump from a crashed production instance, which is located at `/home/user/dump.txt`.

Your objectives:
1. Identify and fix the environment misconfiguration so that `/home/user/repo/test.sh` can execute successfully. (Note: the script expects a specific environment variable to be set to a specific path).
2. Use `git bisect` (or a manual bisection) using `test.sh` to find the exact commit hash that introduced the regression. The first commit in the repo is known to be good, and the latest commit (HEAD) is known to be bad.
3. Analyze the memory dump `/home/user/dump.txt` to identify the fully qualified name of the Go function that is blocking and causing the leak.

Once you have identified the culprit commit and the leaking function, write your findings to `/home/user/solution.txt`. 

The file `/home/user/solution.txt` must have exactly the following format (replace the placeholders with your discovered values):
Commit: <full_40_character_commit_hash>
Function: <fully_qualified_function_name>

Example of function name: `leaktest.myBadFunction`