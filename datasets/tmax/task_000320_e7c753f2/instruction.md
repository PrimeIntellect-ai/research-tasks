You have just inherited an unfamiliar, legacy data processing pipeline written entirely in Bash. The pipeline processes simulated financial transactions, calculating statistical summaries. Recently, downstream consumers reported a statistical anomaly: the calculated daily average is significantly skewed, and certain transaction records seem to be silently dropping out of the pipeline.

The codebase is located in a Git repository at `/home/user/legacy_pipeline`. 
There is a test script `/home/user/legacy_pipeline/run_pipeline.sh` that processes a static dataset `/home/user/legacy_pipeline/data/transactions.csv` and outputs statistics to `/home/user/legacy_pipeline/output/stats.txt`. It also generates three separate log files representing different stages of the pipeline:
- `/home/user/logs/ingest.log`
- `/home/user/logs/process.log`
- `/home/user/logs/export.log`

Your tasks are:
1. **Git Bisection:** The bug was introduced sometime in the last 20 commits. The commit tagged `v1.0` is known to be good (no statistical skew, average is around 0). The `main` branch HEAD is bad (average is highly skewed). Use `git bisect` to identify the exact commit hash that introduced the bug.
2. **Interactive Debugging & Fix:** Analyze the bad commit. Identify the Bash script and the exact line of code that causes the bug (it drops negative transactions). Fix the bug on the `main` branch so that `run_pipeline.sh` produces the correct statistics again.
3. **Log Timeline Reconstruction:** Run the fixed pipeline. Reconstruct the timeline of transactions across the three log files. Find the transaction ID of the first transaction in the dataset (which previously dropped but now succeeds) that is negative. 

Write your final findings to `/home/user/solution.txt` in exactly the following format:
```
BAD_COMMIT=<full_git_commit_hash>
BUG_FILE=<relative_path_to_buggy_file>
DROPPED_TX_ID=<transaction_id>
```

Finally, ensure that the code on the `main` branch of `/home/user/legacy_pipeline` is fixed and fully committed with the message "Fix statistical anomaly".