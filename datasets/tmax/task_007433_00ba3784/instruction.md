You are a DevOps engineer tasked with debugging a Python asynchronous service located at `/home/user/service`. 

Recently, we noticed that the service leaks memory—specifically, `asyncio` tasks keep accumulating when client requests are cancelled before completion. We have provided a test script at `/home/user/test_leak.py` that checks for this exact leak. 

However, things are currently broken:
1. The test script `test_leak.py` currently crashes because of a recent environment misconfiguration in the service's dependencies or configuration files.
2. We don't know exactly when the leak was introduced.

Your objectives:
1. **Fix the misconfiguration**: Repair the environment/configuration so that `/home/user/test_leak.py` can execute and accurately report the leak. You may modify the environment or configuration files as needed.
2. **Find the regression**: Use `git bisect` (or any other method) in the `/home/user/service` repository to find the exact commit that introduced the task leak. Write the full 40-character commit hash of the bad commit to `/home/user/bad_commit.txt`.
3. **Fix the bug**: Identify why the tasks are leaking upon cancellation and fix the code in `server.py`. Once fixed, `test_leak.py` should pass without detecting any leaked tasks.
4. **Create a patch**: Save your code fix as a unified diff patch file at `/home/user/fix.patch`. The patch should apply cleanly to the latest codebase.

Ensure that `/home/user/bad_commit.txt` contains exactly the bad commit hash and nothing else.