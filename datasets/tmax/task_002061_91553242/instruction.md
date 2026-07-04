You are a data analyst and system engineer tasked with migrating a slow, batch-oriented anomaly detection pipeline into a high-performance, real-time streaming service in C.

Currently, we rely on a legacy, stripped, black-box binary located at `/app/detector.bin` to identify anomalies in time-series data. The binary takes exactly four floating-point numbers as command-line arguments, representing three historical time-bucket averages and the current time-bucket average (in chronological order: `history1 history2 history3 current`). It evaluates the sequence and prints either `ANOMALY` or `NORMAL` to standard output. 

Because invoking a binary for every data point is too slow, you need to:
1. **Reverse-engineer the logic** of `/app/detector.bin` by experimenting with it. It implements a deterministic, relatively simple mathematical threshold based on the inputs.
2. **Implement a real-time streaming TCP server in C**. The server must:
   - Listen on `127.0.0.1:7777`.
   - Accept incoming TCP connections.
   - Read streaming ASCII CSV data from the client, formatted as `timestamp,value\n` (where `timestamp` is an integer UNIX epoch time and `value` is a float). The timestamps will arrive in strictly increasing order.
3. **Bucket and Aggregate**:
   - Group the incoming data into 10-second non-overlapping windows. The bucket's start time is aligned to the epoch (e.g., `ts_start = (timestamp / 10) * 10`).
   - Calculate the arithmetic mean (average) of the values in each bucket.
4. **Evaluate and Respond**:
   - The moment a data point arrives with a timestamp belonging to a *new* bucket, the previous bucket is considered finalized.
   - Upon finalizing a bucket, evaluate it using the mathematical logic you reverse-engineered from `/app/detector.bin`. (Note: The first 3 finalized buckets of a session cannot be evaluated for anomalies because there is insufficient history. Treat them as `NORMAL`).
   - Immediately write a response back to the TCP client for the finalized bucket in the format: `BUCKET <ts_start> <avg_value> <ANOMALY|NORMAL>\n`. Format the average to exactly 2 decimal places.
   - When the client closes the connection, finalize the last pending bucket (if any) and evaluate it.
5. **Pipeline Logging**:
   - Append a log entry to `/home/user/pipeline.log` for every finalized bucket in the exact format: `[INFO] Processed bucket <ts_start>, avg: <avg_value>, status: <status>\n`.

Your final C source code should be saved at `/home/user/server.c` and compiled to `/home/user/server`. Ensure the server is left running in the background so it can be tested. You may write auxiliary scripts in Python, Bash, etc., to help you reverse-engineer the binary.