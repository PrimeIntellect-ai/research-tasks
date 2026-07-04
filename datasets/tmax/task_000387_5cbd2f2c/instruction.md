You are a site reliability engineer investigating a critical regression in our custom Bash-based database engine. The production system recently crashed, and we need your help to isolate the cause, recover lost data, and find a leaked secret.

The engine source code is located in the Git repository at `/home/user/db_engine`. 
The `main` branch is currently failing, while the tag `v1.0` is known to be stable. There are approximately 200 commits between `v1.0` and `main`.

Here is your objective:
1. **Bisect the Regression**: Write a minimal Bash test script and use `git bisect` to identify the exact commit hash that introduced the bug causing the engine to fail.
2. **Recover a Leaked Secret**: The developer who introduced the bug tried to debug it in subsequent commits and accidentally hardcoded a recovery password into a script. They removed it shortly after, but it remains in the Git history near the bad commit. Find the value assigned to `RECOVERY_PASS`.
3. **Database Recovery**: The crash corrupted the production database located at `/home/user/data/prod.db`. The uncommitted transactions are located in `/home/user/data/prod.db.wal`. The `.wal` file is a custom text-based write-ahead log. Use the recovered `RECOVERY_PASS` to process the valid entries in the `.wal` file (the valid format and encryption/encoding rules are documented in the `db_read.sh` script in the repo) and find the final value of the `ADMIN_USER` key.

Create a final report at `/home/user/report.txt` with exactly three lines in the following format:
Line 1: The full Git commit hash of the first bad commit
Line 2: The recovered RECOVERY_PASS value
Line 3: The recovered value for the ADMIN_USER key from the database

Note: You are limited to using Bash, coreutils, and standard Unix CLI tools (like awk, sed, grep, git).