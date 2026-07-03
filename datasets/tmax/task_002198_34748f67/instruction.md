You are a log analyst investigating sudden latency spikes in a global application. The application logs are stored in a UTF-8 encoded JSON-lines file at `/home/user/app_logs.jsonl`. Each line represents a single event and contains mixed-language log messages.

Your goal is to write a Python script to detect the first processing anomaly (changepoint) based on rolling statistics and analyze the Unicode message that caused it. 

Here are your specific instructions:
1. Parse `/home/user/app_logs.jsonl`. Each line is a JSON object with keys: `timestamp`, `message`, and `processing_time_ms`.
2. Compute rolling statistics for `processing_time_ms`. Maintain a rolling window of the strictly previous 30 valid entries (do not include the current entry in the window). 
3. Begin checking for anomalies only when your rolling window is fully populated (i.e., starting at the 31st log entry, which is index 30 if 0-indexed).
4. An anomaly is defined as the **first** log entry where `processing_time_ms` is strictly greater than `(rolling_mean + 5 * rolling_std_dev)`. Use the sample standard deviation.
5. Once you find the first anomaly, stop. Extract the `message` field from this anomalous entry.
6. Calculate the length of the `message` in characters (Unicode code points) and its length in UTF-8 bytes.
7. Save the results of this first anomaly to `/home/user/anomaly.json` in exactly this format:
```json
{
  "index": <0-based integer index of the anomalous line>,
  "timestamp": "<timestamp string>",
  "message_char_len": <integer length in chars>,
  "message_byte_len": <integer length in bytes>
}
```

Ensure your script is self-contained and only uses Python standard libraries (e.g., `json`, `statistics`). Run your script to generate the output file.