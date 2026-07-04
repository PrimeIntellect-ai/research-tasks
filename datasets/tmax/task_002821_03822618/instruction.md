You have been given access to a Git repository at `/home/user/repo` containing a C program called `data_parser`. 

Recently, a regression was introduced that causes the program to crash when processing files with spaces in their names. The test suite (`make test`) currently fails on the `main` branch with a segmentation fault.

Your tasks are:
1. **Bisect the Regression:** The commit tagged `v1.0` is known to be good. Use `git bisect` (or any delta debugging strategy) to identify the exact commit that introduced the bug. Write the full 40-character commit hash to `/home/user/bad_commit.txt`.
2. **Core Dump Analysis:** The crash occurs when the program tries to process a specific input file. Run the program such that it produces a core dump. Using `gdb` or another tool, analyze the core dump to find the value of the local variable `secret_key` inside the `process_file` function at the time of the crash. Write the exact string value of this variable to `/home/user/recovered_key.txt`.
3. **Fix the Bug:** On the `main` branch, fix the bug in `data_parser.c` so that the program handles files with spaces correctly without crashing, even if they lack file extensions. Ensure that `make test` completes successfully. Do not remove any functionality; just fix the crash.

Constraints:
- You must work within `/home/user/repo`.
- Do not modify the test cases in the `Makefile`.
- Make sure core dumps are enabled (`ulimit -c unlimited`) before generating the crash.