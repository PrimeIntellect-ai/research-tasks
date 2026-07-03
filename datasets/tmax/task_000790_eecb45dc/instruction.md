You are tasked with debugging a failing build and recovering lost data for a multi-language project (C and Python). The project is located in `/home/user/app_repo`. 

Recently, the CI pipeline has been failing intermittently during the test phase. Your objectives are:

1. **Root Cause Analysis & Git Bisection**: Find the specific git commit that introduced the intermittent bug. Write the full 40-character commit hash to `/home/user/bad_commit.txt`.
2. **Interactive Debugging & Fixing**: Investigate the C code (`processor.c`) used by the Python application. The bug causes intermittent test failures (often related to memory access). Fix the bug in `processor.c` so that `make test` reliably passes.
3. **Regression Testing**: Create a new test file `/home/user/app_repo/regression_test.py` that reliably reproduces the failure on the buggy commit, but passes on your fixed version. It should exit with code 0 on success and non-zero on failure.
4. **Database Recovery**: The bug previously caused a crash, leaving a corrupted SQLite database. In `/home/user/db_crash/`, you will find `app.db` and `app.db-wal`. Recover the database data and dump the full SQL (schema and data) to `/home/user/recovered.sql`. 

Ensure all your fixes are committed to the git repository on the main branch before finishing.