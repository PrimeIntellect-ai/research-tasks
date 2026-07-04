You are acting as a Site Reliability Engineer (SRE). Our custom Service Level Indicator (SLI) metric aggregator, which calculates rolling uptime and latency statistics from ping logs, has been crashing and reporting incorrect mathematical results.

You need to debug and fix the aggregator script located at `/home/user/metric_aggregator.py`.

The script reads a JSONL file containing ping logs and is expected to calculate the cumulative uptime percentage and a 5-ping rolling average of latency for each entry. It should output a JSON array of these calculated metrics to a file.

However, the script has a few issues:
1. **Serialization Error:** It crashes when trying to write the final output because it doesn't correctly handle Python `datetime` objects during JSON serialization.
2. **Mathematical Formula Error:** The formula calculating the cumulative uptime percentage is mathematically incorrect. It should be the ratio of successful pings to the total number of pings processed so far, expressed as a float between 0.0 and 1.0.
3. **Boundary Condition (Off-by-one/Index wrapping):** The rolling average of the latency for the last 5 pings is incorrect during the first 4 pings. Because of negative indexing in Python slicing, it is accidentally including data from the *end* of the list.

Your task:
1. Identify and fix the bugs in `/home/user/metric_aggregator.py`.
2. Run the fixed script on the log file: `/home/user/ping_logs.jsonl`.
3. The script must successfully write the output to `/home/user/metrics.json`.

The output file `/home/user/metrics.json` must contain a valid JSON array of objects. Each object must have:
- `timestamp`: string (ISO 8601 format)
- `cumulative_uptime`: float (0.0 to 1.0)
- `rolling_latency_avg`: float (average latency of up to the last 5 pings, including the current one. If there are fewer than 5 pings so far, average whatever is available).

Do not change the command-line arguments the script expects.