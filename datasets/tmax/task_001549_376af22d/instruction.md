You are a log analyst investigating anomalous patterns in a high-throughput server. Your team relies on a legacy C++ tool, located at `/app/legacy_detector`, to process JSON-lines server logs, extract metrics, and flag anomalies. 

Unfortunately, `/app/legacy_detector` has a critical flaw: it occasionally segfaults on extremely large files. We need to rewrite this tool in Python, ensuring **bit-exact compatibility** with its output so it can act as a drop-in replacement in our pipeline.

We have managed to recover the high-level specification of what the binary does:
1. **Input:** Reads JSON-lines from standard input (`stdin`). Each line is a JSON object with three keys: `"ts"` (integer timestamp), `"metric"` (float or null), and `"msg"` (string).
2. **Robust Parsing:** The legacy JSON parser replaces any invalid unicode escape sequences (e.g., `\uXXXX` where XXXX is not a valid hex code) in the `"msg"` field with the standard replacement character `?`. 
3. **Imputation:** If `"metric"` is null or missing, it performs forward-fill imputation (uses the most recently seen valid metric value). If the very first entries are null, it leaves them as null until a valid metric is found.
4. **Windowed Aggregation:** Calculates a rolling mean and rolling standard deviation of the metric over a strictly trailing window of size `W=5` (including the current element, using sample standard deviation).
5. **Anomaly Detection:** Flags the current entry as an anomaly (`true` or `false`) if the absolute difference between the current metric and the rolling mean is strictly greater than `2.0 * rolling_std`. If the window has fewer than 2 elements (making std dev undefined) or the metric is still null, anomaly is `false`.
6. **Output:** Writes a CSV to standard output (`stdout`) with the header `ts,metric,mean,std,anomaly,clean_msg`. Floats are formatted to exactly 4 decimal places. Null values are printed as empty strings.

Your task is to write a Python script at `/home/user/detector.py` that reads from `stdin` and writes to `stdout`. Its behavior must be **bit-exact identical** to `/app/legacy_detector`. 

You can test the legacy binary by passing it sample JSONL data:
`echo '{"ts": 1, "metric": 5.0, "msg": "test\\uZZZZ"}' | /app/legacy_detector`

Write the Python replacement to be robust, efficient, and perfectly matching the legacy output.