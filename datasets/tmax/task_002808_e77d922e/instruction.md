You are tasked with diagnosing and fixing a regression in a Python data processing tool.

The tool is located in a Git repository at `/home/user/repo`.
Between tag `v1.0` (which worked perfectly) and tag `v2.0` (the current `main` branch HEAD), a regression was introduced. When running the tool on a large dataset, the script indefinitely hangs and makes no progress.

You can find a sample input file that triggers this hang at `/home/user/data/input.txt`.
You can run the script using: `python process.py /home/user/data/input.txt`

Your tasks are:
1. **Bisect the regression**: Find the exact commit that introduced the hang. You may need to use system call tracing (`strace`), an interactive debugger, or a timeout-based script to automate the bisection.
2. Write the full 40-character Git commit hash of the bad commit to `/home/user/bad_commit_hash.txt`.
3. **Fix the bug**: On the current `main` branch (at tag `v2.0`), edit `process.py` to fix the hanging issue without altering the intended data processing functionality (the script uses a subprocess to transform the input data).
4. Run your fixed script on `/home/user/data/input.txt` and save its standard output to `/home/user/fixed_output.txt`.

Ensure your fix handles large amounts of data robustly without deadlocking. Do not change the external command the script invokes, just fix the Python code interacting with it.