You are tasked with fixing and completing a time-series data pipeline for a configuration manager tracking system. 

In `/home/user/config_tracker`, there is a raw CSV file named `changes.csv`. This file logs configuration updates across different servers over time. 
The columns are: `timestamp,server_id,config_key,config_value,size_bytes`

However, the pipeline has several critical issues and missing features that you need to resolve using standard Linux CLI tools and Bash (e.g., `awk`, `sed`, `grep`, GNU coreutils):

1. **Embedded Newlines**: The `config_value` column frequently contains multi-line JSON or text enclosed in double quotes. A naive line-by-line parser silently breaks or drops these rows. You must correctly parse the CSV, preserving rows with embedded newlines. 
2. **Standardization**: The `config_key` values are inconsistently formatted. You must normalize them by converting all letters to lowercase and replacing any spaces with underscores (e.g., "Max Connections" becomes "max_connections").
3. **Rolling Aggregation**: For each `server_id` (processed chronologically by `timestamp`), calculate a rolling 3-event moving average of the `size_bytes`. The window should include the current event and up to 2 previous events for that specific server. (For the first event, the average is just its own size; for the second, the average of the first two). Calculate this as an integer (floor the result).
4. **Anomaly Detection**: Compare the current event's `size_bytes` against its newly calculated rolling average. If the current `size_bytes` is strictly greater than `2.0 * rolling_average`, flag it as an anomaly.

Write a Bash script (or pipeline) that reads `/home/user/config_tracker/changes.csv`, performs the above transformations, and outputs the result to `/home/user/config_tracker/processed_anomalies.csv`.

The output CSV must have the following exact headers and format:
`timestamp,server_id,normalized_config_key,size_bytes,rolling_avg,is_anomaly`

Where:
- `timestamp`: The original timestamp.
- `server_id`: The original server ID.
- `normalized_config_key`: The standardized config key.
- `size_bytes`: The original size in bytes.
- `rolling_avg`: The computed 3-event moving average (integer/floored).
- `is_anomaly`: "YES" if `size_bytes > 2 * rolling_avg`, otherwise "NO".

The output must be sorted chronologically by `timestamp`, then by `server_id` if timestamps match. Ensure you strip out the `config_value` column entirely in the final output. 

Note: You have `sudo` privileges to install tools like `gawk`, `csvkit`, or `miller` if you prefer them over writing a custom Bash state machine, but the final wrapper must be executable from the terminal.