You are a Site Reliability Engineer (SRE) investigating a recent outage in your uptime monitoring system. The metrics processing worker crashed unexpectedly, leaving behind a stack trace and an un-checkpointed SQLite database. 

You need to perform a forensic investigation to find the exact regression that caused this crash, using the data left behind.

Here is the current state of your system:
- **Git Repository:** `/home/user/app_repo` contains the source code for the metric processor (`processor.py`). The repository has a linear history. 
- **Crash Log:** `/home/user/crash.log` contains the stack trace from the crash.
- **Database:** `/home/user/data/` contains `metrics.db`, `metrics.db-wal`, and `metrics.db-shm`. The crash happened immediately upon receiving a "poison pill" metric, which was written to the Write-Ahead Log (WAL) but the process died before handling it properly.

Your tasks are:
1. **Analyze the Crash & Database:** Read the stack trace and recover the SQLite database. Query the `metrics` table to find the `id` of the most recently received metric (the one with the highest `id`). This is the "poison pill" that crashed the system.
2. **Identify the Regression:** The bug was introduced recently. Write a short Python test script that imports `processor.py` and processes the poison pill metric (using its `name` and `value` from the database). 
3. **Bisect:** Use `git bisect` (along with your test script) in the `/home/user/app_repo` repository to find the exact commit hash that introduced the crash. The first commit in the repository is known to be `good`, and the `HEAD` commit is known to be `bad`.
4. **Report:** Create a file at `/home/user/report.txt` containing exactly two lines in this format:
```
Commit: <bad_commit_hash>
Poison ID: <poison_pill_id>
```

Ensure the file contains the full 40-character Git commit hash.