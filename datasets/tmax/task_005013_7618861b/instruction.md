You are tasked with building a configuration processing service for our infrastructure management system. 

We receive streams of configuration metrics from various servers, but the data is often noisy, contains duplicates, and has missing data points due to network drops.

Your goal is to build an HTTP service in Python that processes these metrics in real-time.

Requirements:
1. Create a Python HTTP server listening on `127.0.0.1:8080`.
2. It must expose a `POST /process` endpoint that accepts a JSON payload. The payload is a JSON array of configuration metric objects.
   Example object: `{"timestamp": 1600000000, "cpu": 2.5, "mem": 1024.0, "config_id": "svr1-revA"}`. Note that `cpu` and `mem` can be `null` (missing).
3. **Deduplication**: First, sort the array by `timestamp` ascending. Then, deduplicate the records based on their `config_id`. To do this, you must use a proprietary hashing algorithm. We have provided a compiled Linux binary at `/app/config_hasher`. 
   - Usage: `/app/config_hasher <config_id>`
   - It outputs a 32-character hexadecimal string.
   - You must compute this hash for each `config_id`. If multiple records yield the *same* hash, keep only the first one (chronologically) and discard the rest.
4. **Imputation**: For the deduplicated time series, fill in any `null` values for `cpu` and `mem`. 
   - Use linear interpolation based on the `timestamp` differences. 
   - If the very first or very last values are missing, use backward-fill or forward-fill, respectively.
5. **Rolling Aggregation**: After imputation, compute a 3-item moving average for both `cpu` and `mem`.
   - The moving average at index `i` should be the average of the items at indices `i-2`, `i-1`, and `i`.
   - For the first item (index 0), the average is just the item itself. For the second item (index 1), the average is the mean of index 0 and 1.
6. **Response**: The endpoint must return a JSON array of objects, corresponding to the deduplicated and processed records, in chronological order. Each object must have the following keys:
   - `timestamp` (integer)
   - `cpu_imputed` (float, rounded to 2 decimal places)
   - `mem_imputed` (float, rounded to 2 decimal places)
   - `cpu_rolling_avg` (float, rounded to 2 decimal places)
   - `mem_rolling_avg` (float, rounded to 2 decimal places)

Ensure your service remains running so we can test it. You can use standard libraries or install `pandas`, `fastapi`, `uvicorn`, `Flask`, etc., if you prefer.