We have a legacy compiled tool located at `/app/config_drift_analyzer` that processes raw configuration change logs from our fleet of servers. These logs are time-series data representing configuration metrics (e.g., memory limits, connection pool sizes) over time. We need to deprecate this binary and replace it with a Python implementation, but the source code is lost. 

Your task is to write a Python 3 script at `/home/user/drift_analyzer.py` that behaves EXACTLY like the legacy binary.

You can run `/app/config_drift_analyzer <input.csv> <output.json>` to observe its behavior. 

Here is what we know about the expected data processing pipeline:
1. **Input Format:** A CSV file with headers: `server_id,timestamp,metric_name,value`. The `value` column may contain floating-point numbers or be empty (representing missing data).
2. **Validation:** Rows with negative `timestamp` values or missing `server_id`/`metric_name` must be dropped entirely.
3. **Sorting and Grouping:** The data must be grouped by `server_id`. Within each group, records must be sorted by `timestamp` in ascending order.
4. **Interpolation & Imputation:** For missing `value` entries within a specific `server_id` and `metric_name` series, the program must apply linear interpolation. If missing values occur at the very beginning or end of the series where linear interpolation isn't strictly bounded by two points, it should fall back to a forward-fill (carrying the last known value forward), or backward-fill for leading gaps.
5. **Output Format:** The final output must be a tightly packed JSON object (no extra whitespace, keys sorted alphabetically) written to the specified output file path. The JSON structure maps `server_id` -> `metric_name` -> list of `[timestamp, imputed_value]` pairs. Note: `imputed_value` should be rounded to exactly 4 decimal places.

Your script must accept two positional arguments:
`python3 /home/user/drift_analyzer.py <input_file.csv> <output_file.json>`

We will verify your solution by fuzzing both your Python script and the legacy binary with thousands of randomly generated input CSVs and ensuring their JSON outputs are bit-for-bit identical.