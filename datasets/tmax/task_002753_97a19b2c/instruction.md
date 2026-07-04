You are a log analyst investigating patterns in a massive stream of access logs. We have an opaque, proprietary log emitter located at `/app/log_emitter` (a stripped binary) that outputs a simulated historical log stream to standard output.

Your task is to build a high-performance data processing pipeline (in a language of your choice) to parse, clean, deduplicate, and aggregate these logs. 

Specifically, your pipeline must do the following:
1. **Pipeline Execution**: Execute `/app/log_emitter` and stream its standard output.
2. **Regex Parsing**: Parse each line using regex. Valid logs follow this general pattern:
   `[{ISO-8601-TIMESTAMP}] {USER_ID} {ACTION} ... bytes={BYTES_TRANSFERRED}`
   Example: `[2023-10-01T10:05:00] user_73 LOGIN src=10.0.0.1 bytes=1024`
   Discard any lines that do not match this structure or cannot be parsed.
3. **Hash-Based Deduplication**: The emitter sometimes outputs duplicate events due to upstream network retries. Compute an MD5 hash of the concatenated string `{TIMESTAMP}{USER_ID}{ACTION}`. Keep only the *first* occurrence of each hash; discard subsequent duplicates.
4. **Windowed Rolling Aggregation**: For each distinct `{USER_ID}`, maintain a 5-minute rolling window of the `bytes` transferred. For every valid, deduplicated log entry, calculate the average `bytes` over the preceding 5 minutes (including the current event, i.e., events in the range `[current_time - 5 minutes, current_time]`).
5. **Data Stratification & Sampling**: We only need a stratified sample for downstream systems. For each user, output every 10th valid deduplicated log entry (i.e., the 1st, 11th, 21st, etc., in chronological order for that user).
6. **Logging**: Maintain pipeline metrics and write them to `/home/user/pipeline_metrics.json` at the end of execution. Format: `{"total_lines_read": X, "valid_parsed_lines": Y, "deduplicated_lines": Z}`.

Output the sampled rolling averages to `/home/user/rolling_averages.csv` with the exact header:
`timestamp,user_id,action,bytes,rolling_avg_bytes`
(Format `rolling_avg_bytes` to 2 decimal places).

Your pipeline's accuracy will be graded against a canonical reference implementation. Your rolling averages must be highly accurate.