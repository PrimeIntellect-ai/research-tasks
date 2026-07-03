**URGENT: 3AM PagerDuty Alert - Financial Pipeline Drift**

You are the on-call engineer. It's 3:00 AM, and our overnight trade aggregation pipeline is failing its data integrity checks due to severe precision loss. The alert indicates that the calculated daily exposure is drifting by several dollars, violating strict accounting thresholds. 

The pipeline code is located in a Git repository at `/home/user/trade_pipeline`. 
We know the pipeline was perfectly healthy at the `v1.0` tag, but the current `HEAD` of the `main` branch is failing. 

Your tasks:
1. Navigate to `/home/user/trade_pipeline`.
2. Use `git bisect` to identify the exact commit that introduced the precision loss regression. You can use the provided script `python /home/user/trade_pipeline/validate_run.py` to test if a commit is good or bad. It will exit with `0` if the precision is within bounds, and `1` if it detects drift or a stack trace error.
3. Analyze the diff of the offending commit to understand the data transformation bug. Someone likely tried to optimize memory or speed but truncated the precision of a critical accumulator.
4. Once you have found the culprit:
   - Write the exact, full Git commit hash of the first bad commit to `/home/user/bad_commit.txt`.
   - Write the exact name of the Python variable that had its precision reduced (e.g., changed from float64/Decimal to float32) to `/home/user/culprit_variable.txt`.

Fixing the code is not required; we just need the diagnostic information for the post-mortem so the trading desk can authorize a rollback.