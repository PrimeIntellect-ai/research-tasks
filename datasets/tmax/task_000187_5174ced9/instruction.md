You are an automation specialist building a robust data pipeline. We have a continuous feed of transaction data stored in a large JSONL (JSON Lines) file located at `/home/user/telemetry.jsonl`. Because this file can grow very large in production, your solution must stream the file (process it line-by-line) rather than loading it entirely into memory.

Your task is to write a script in any language you choose to process this file, enforce data constraints, and detect changepoints/anomalies in the data flow.

**Requirements:**

1. **Constraint-Based Validation:**
   Process `/home/user/telemetry.jsonl` line by line. Every line must meet ALL the following constraints to be considered "valid":
   * Must be well-formed JSON.
   * Must contain exactly these three keys: `tx_id` (integer), `amount` (float or integer), and `status` (string).
   * The `amount` value must be strictly greater than or equal to `0`.
   
   If a line fails *any* of these constraints, it is considered "invalid". You must append the exact, raw, unmodified string of the invalid line to a new file at `/home/user/invalid_records.jsonl`.

2. **Changepoint/Anomaly Detection:**
   For all *valid* records, you need to monitor the `amount` field to detect sudden spikes. 
   * Maintain a moving average of the `amount` of the **last 50 valid records**.
   * You cannot detect a changepoint until you have successfully processed exactly 50 valid records (so the 51st valid record is the first one that could potentially be an anomaly).
   * A changepoint occurs when a valid record's `amount` is strictly greater than `3.0` times the moving average of the *preceding* 50 valid records.
   * When a changepoint is detected, append its `tx_id` (just the integer, one per line) to `/home/user/changepoints.txt`.
   * **Crucial:** A record that is flagged as a changepoint is still a *valid* record, and its `amount` *must* be included in the moving average calculation for subsequent records.

Write and execute your code to process the file and generate the two output files (`/home/user/invalid_records.jsonl` and `/home/user/changepoints.txt`).