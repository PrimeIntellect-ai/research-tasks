You are an automation specialist creating an anomaly detection workflow for server logs. You have been given a continuously growing log file at `/home/user/system_events.log`. To prevent memory exhaustion, you must process this file using a streaming approach (reading line-by-line).

Your task is to write a Python script that processes this log file to identify minutes with an abnormally high variety of event types.

Here are the specific requirements:
1. **Streaming & Parsing**: Read `/home/user/system_events.log` line-by-line. Each line has the format: `[YYYY-MM-DD HH:MM:SS] LEVEL - Message`. Extract the minute (e.g., `2023-10-24 10:05`) and the `Message`.
2. **Tokenization & Normalization**: For each message, normalize it by:
   - Converting to lowercase.
   - Removing all non-alphanumeric characters (keep spaces).
   - Replacing multiple consecutive spaces with a single space.
   - Trimming leading/trailing whitespace.
3. **Hash-Based Deduplication**: Compute the SHA256 hash of each normalized message. Use this hash to determine the number of *unique* event types that occurred within each minute.
4. **Rolling Statistics**: Compute a 3-minute rolling average of the unique event count. For any given minute `T`, the rolling average is the mean of the unique event counts for `T`, `T-1 minute`, and `T-2 minutes`. (Note: If a minute has no logs, its unique count is 0. Assume the log is chronological. You must compute the rolling average starting from the first minute present in the log).
5. **Output**: Save the results to `/home/user/anomalies.json` containing a list of JSON objects for every minute where the 3-minute rolling average is **strictly greater than 3.0**. The JSON should be formatted exactly like this:
   ```json
   [
     {"minute": "2023-10-24 10:15", "rolling_avg": 3.33},
     {"minute": "2023-10-24 10:16", "rolling_avg": 4.0}
   ]
   ```
   *Note: Round `rolling_avg` to 2 decimal places.*

Please create and run the Python script to generate the output file.