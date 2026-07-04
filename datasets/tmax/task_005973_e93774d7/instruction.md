You are the on-call engineer and just received a 3 AM page. The anomaly detection system for the payments pipeline is firing constantly, claiming that the rolling average of request processing times has spiked above the 200ms threshold. However, spot-checking individual logs shows completely normal latencies (around 150-180ms).

You suspect there is a bug in the alerting aggregator script causing a statistical anomaly due to off-by-one errors or boundary condition mishandling.

Your environment contains the following in `/home/user/oncall`:
1. `frontend.log` - JSONL file containing incoming request logs (`ts`, `req_id`, `endpoint`).
2. `backend.log` - JSONL file containing backend processing logs (`ts`, `req_id`, `proc_time_ms`). Note that these logs are collected asynchronously and may be out of order.
3. `aggregator.py` - The Python script responsible for joining these logs, reconstructing the timeline, computing a 10-request sliding window average of `proc_time_ms`, and alerting if the average exceeds 200ms.

Your tasks:
1. Reconstruct the timeline: Understand how `aggregator.py` merges the logs across the two services.
2. Debug the anomaly: Find and fix the off-by-one and boundary condition errors in the sliding window calculation within `aggregator.py` that are artificially inflating the rolling average.
3. Run the fixed script on the provided logs:
   `python /home/user/oncall/aggregator.py /home/user/oncall/frontend.log /home/user/oncall/backend.log > /home/user/oncall/fixed_anomalies.jsonl`

Requirements for the fix:
- The sliding window must contain *at most* `window_size` elements.
- The average must be calculated using the *actual* number of elements in the current window (which will be less than `window_size` during the initial startup boundary).
- Do not modify the input log files.
- The output file `/home/user/oncall/fixed_anomalies.jsonl` must be a valid JSONL file containing the merged records with the correct `rolling_avg`.