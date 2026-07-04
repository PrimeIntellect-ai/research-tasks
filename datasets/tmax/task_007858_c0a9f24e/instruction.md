You are a log analyst investigating performance patterns in a web service. You have a JSON Lines log file containing request timestamps and latencies, but it has missing periods (gaps) and high variance. 

Your task is to write a Bash script `/home/user/analyze.sh` that processes `/home/user/requests.jsonl` and produces a CSV report at `/home/user/rolling_latency.csv`.

Here are the requirements for your script:
1. **Read JSONL**: The input file `/home/user/requests.jsonl` contains lines like `{"ts": 1600000002, "lat": 10}` where `ts` is a Unix timestamp (integer) and `lat` is latency in milliseconds (integer).
2. **Resample and Gap-Fill**: 
   - Group the logs into 10-second intervals based on the timestamp (e.g., `ts` from 1600000000 to 1600000009 belongs to the interval 1600000000).
   - The output must include an entry for every 10-second interval from the *minimum* interval present in the file to the *maximum* interval present in the file, inclusive.
   - If an interval has no logs, its request count is 0 and the average latency for that interval is 0.00.
3. **Rolling Aggregation**:
   - Calculate a 30-second moving average (`mavg_30s`) of latency. This is the sum of latencies over the current interval and the previous two intervals, divided by the total request count over those three intervals.
   - If the total request count over the 3 intervals is 0, the moving average should be 0.00.
4. **Output Format**:
   - Write to `/home/user/rolling_latency.csv`.
   - The file must have a header: `interval_ts,count,avg_lat,mavg_30s`
   - `interval_ts` is the start of the 10-second bucket.
   - `count` is the number of requests in that bucket.
   - `avg_lat` is the average latency of requests in that bucket, formatted to exactly 2 decimal places.
   - `mavg_30s` is the 30-second moving average latency as described, formatted to exactly 2 decimal places.

Your script must run successfully when executed as `bash /home/user/analyze.sh`. Ensure you use standard CLI tools available on Linux (like `jq`, `awk`, `sort`, etc.).