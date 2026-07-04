You are a data engineer responsible for building an ETL and anomaly detection pipeline. We have a legacy proprietary sensor stream generator located at `/app/sensor_stream`. This is a compiled binary that outputs 100,000 rows of CSV data (headers: `timestamp,value`) to standard output when executed.

Your task consists of the following phases:

1. **Extract and Load**:
   - Execute the `/app/sensor_stream` binary and capture its output.
   - Bulk import this raw CSV data into a new SQLite database located at `/home/user/metrics.db` within a table named `readings`.

2. **Transform and Detect** (using Python):
   - Write a Python script to query the SQLite database and perform a windowed rolling aggregation. Calculate a rolling mean and rolling standard deviation using a trailing window of exactly **200** periods (inclusive of the current row). Do not calculate rolling stats for the first 199 rows (they should be ignored for anomaly detection).
   - Flag a data point as an anomaly if the absolute difference between its `value` and the 200-period rolling mean is strictly greater than **4 times** the 200-period rolling standard deviation.
   - Save the `timestamp` values of all detected anomalies as a flat JSON array of integers in `/home/user/anomalies.json`.
   
3. **Template-Based Reporting**:
   - Create a Python script that uses string templating (or a library like Jinja2 if you install it) to generate a summary report at `/home/user/report.html`.
   - The HTML report must include the total number of anomalies inside a tag exactly like this: `<div id="anomaly-count">TOTAL_COUNT</div>` (replace TOTAL_COUNT with your calculated integer).

The automated verification system will evaluate your `/home/user/anomalies.json` output by comparing the timestamps of the anomalies you found against the hidden ground truth. Your algorithm's F1 score must be >= 0.95.