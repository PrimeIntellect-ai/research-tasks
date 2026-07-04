You are acting as a data scientist cleaning up a noisy dataset of server metrics. 

You have two input files in your home directory (`/home/user/`):
1. `metrics.jsonl`: A JSON-lines file containing server metrics. Each line should be a JSON object with at least `timestamp` (integer), `server` (string), and `cpu` (float). However, our logging system had a bug, and some lines contain malformed unicode escape sequences (e.g., incomplete `\u` escapes) which make them invalid JSON.
2. `server_info.csv`: A CSV file containing server metadata with columns `server,role`.

Your task is to write and execute a Python script that does the following:
1. **Multi-format reading & Cleaning:** Read `metrics.jsonl`. You must attempt to parse each line as JSON. If a line raises a JSON decoding error due to the malformed escapes, you must completely skip/drop that line. Do not try to fix the string. Read `server_info.csv` as well.
2. **Merging:** Join the valid metrics data with the `server_info.csv` data on the `server` field.
3. **Windowed Aggregation:** For each `server`, calculate a rolling average of the `cpu` metric over a window of the **last 2 valid records** (including the current record), ordered by `timestamp` ascending. If a server only has 1 record so far, the average is just that record's `cpu` value.
4. **Output:** Save the final joined and aggregated data to `/home/user/clean_metrics.csv`. The output must be a CSV file with the following columns in exactly this order: `timestamp,server,role,cpu,cpu_rolling_avg`. Sort the final CSV by `timestamp` ascending.

Ensure the final CSV has a header row. 
You can use `pandas` (which is installed in the environment) or standard libraries.