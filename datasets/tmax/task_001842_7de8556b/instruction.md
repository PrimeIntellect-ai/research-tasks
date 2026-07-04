You are acting as a DevOps engineer debugging a log processing pipeline. 

We have a concurrent bash-based log aggregator in `/home/user/log_pipeline/`. The main script, `run_all.sh`, reads pairs of log files from `jobs.txt` and spawns a background job for each pair using `merge_logs.sh`. 

Recently, the pipeline has been hanging indefinitely without completing. We suspect there is a deadlock caused by high contention and conflicting resource locking orders.

Your task is to debug and fix this issue:
1. **Analyze and Isolate:** Find the specific pair of jobs (lines) in `jobs.txt` that cause the deadlock. Create a minimal reproducible example by saving exactly one of those two space-separated lines into a file at `/home/user/log_pipeline/mre.txt`. (Just the literal text of the line, e.g., `inputs/appX.log inputs/appY.log`).
2. **Fix the Deadlock:** Modify `/home/user/log_pipeline/merge_logs.sh` to prevent the deadlock. You must ensure that the locks are always acquired in alphabetical order of the file paths, regardless of the order they are passed as arguments.
3. **Add Validation:** Add a bash assertion inside `merge_logs.sh` just before the locking steps to ensure the first file to be locked is alphabetically before or equal to the second file.
4. **Verify:** Run `/home/user/log_pipeline/run_all.sh`. If it runs successfully to completion without deadlocking, it will create `/home/user/log_pipeline/success.log`.

Do not change `run_all.sh` or `jobs.txt`. The fix must exclusively be in `merge_logs.sh`.