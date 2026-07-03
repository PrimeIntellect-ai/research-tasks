You are an AI assistant helping a configuration manager analyze historical cluster changes. 

The configuration manager uses a log file located at `/home/user/config_audit.log` to track configuration updates made to various servers. 
The log file follows this format:
`TIMESTAMP USER SERVER CONFIG_KEY OLD_VALUE NEW_VALUE`
Example:
`2023-10-01T10:00:00Z alice web-01 worker_threads 16 32`

Your task is to process this log file and calculate a rolling statistic to track how the `worker_threads` configuration has evolved over time. You may use any language or shell tools to achieve this.

Perform the following steps:
1. Extract only the lines where `CONFIG_KEY` is exactly `worker_threads`.
2. Convert the `TIMESTAMP` into a standard UNIX epoch timestamp.
3. Calculate a 3-event moving average of the `NEW_VALUE` for `worker_threads`. This means the average of the current `NEW_VALUE` and the two immediately preceding `NEW_VALUE`s for `worker_threads`. Compute this moving average globally across all servers, strictly in the chronological order the events appear in the log.
4. Output only the events starting from the 3rd `worker_threads` change (so that the moving average is calculated using a full window of 3 values).
5. The moving average must be mathematically rounded to the nearest integer (e.g., 40.33 becomes 40, 41.5 becomes 42).
6. Save the final output to a CSV file at `/home/user/worker_threads_ma.csv` with exactly this format (no header):
`EPOCH_TIMESTAMP,SERVER,MOVING_AVERAGE`

Ensure the final CSV strictly matches the requested format and is saved in the correct location.