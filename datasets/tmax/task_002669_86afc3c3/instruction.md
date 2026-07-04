You are a log analyst investigating a massive set of interleaved access logs for suspicious behavior. You have been provided with a large raw log file and an opaque, proprietary compiled binary that scores session anomalies.

Your task is to build a high-performance Bash pipeline (using standard shell built-ins, `awk`, `sed`, `sort`, `xargs`, etc.) to clean the data, reconstruct user sessions, and identify the top 100 most anomalous users. 

**Resources Provided:**
1. **Raw Logs:** Located at `/home/user/raw_logs.txt`. 
   Format (pipe-separated): `Timestamp|UserID|Action|IP`
   Example: `2023-10-01 12:04:01|U9921|LOGIN|192.168.1.5`
2. **Anomaly Scorer:** A stripped binary located at `/app/anomaly_scorer`. It reads session strings from `stdin` and outputs an anomaly score to `stdout`.

**Processing Requirements:**
1. **Cleaning:** Ignore any log lines where the `Action` starts with the string `DEBUG_`.
2. **Sorting & Grouping:** Group the remaining actions by `UserID`, ordered chronologically by `Timestamp`.
3. **Normalization (Deduplication):** Within each user's chronological session, collapse consecutive identical actions into a single action. For example, if a user's chronological actions are `LOGIN, VIEW, VIEW, BUY, VIEW`, it should be normalized to `LOGIN, VIEW, BUY, VIEW`.
4. **Formatting:** Transform the normalized session into a tab-separated string: `UserID\tAction1,Action2,Action3...`
5. **Scoring:** Pipe these formatted strings into `/app/anomaly_scorer`. The binary expects exactly one session per line on standard input. It will output `UserID\tAnomalyScore` for each line it successfully parses.
6. **Final Extraction:** Sort the output of the anomaly scorer by the `AnomalyScore` in descending order. If scores are tied, sort by `UserID` in ascending alphabetical order.
7. **Output:** Write exactly the top 100 results (just `UserID,Score` comma-separated) to `/home/user/top_100_anomalies.csv`.

**Constraints:**
- The log file is extremely large. A naive `while read` loop in pure Bash will be too slow. You must use stream-processing tools like `awk`, `sort`, and pipes.
- Ensure your pipeline correctly handles users with thousands of actions.

Your output will be graded programmatically based on the overlap (Jaccard Index) of your top 100 list against the definitive ground truth, requiring a score of >= 0.99.