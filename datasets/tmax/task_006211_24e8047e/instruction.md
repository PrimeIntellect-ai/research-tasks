You are a data analyst tasked with processing a large batch of server telemetry data.

In the directory `/home/user/telemetry_data/`, there are 50 CSV files named `telemetry_01.csv` through `telemetry_50.csv`. Each file contains raw server metrics recorded over time in a "wide" format. 

The columns in each CSV are:
`timestamp, server_id, cpu_node1, mem_node1, cpu_node2, mem_node2`

However, the data is messy:
1. There are exact duplicate rows in the files due to collection glitches.
2. The `server_id` column has inconsistent formatting (leading/trailing whitespace, mixed casing).
3. Missing values are represented as empty strings or `"NaN"`.

Your task is to write a script in any language you choose to process this data. Because of the hypothetical volume of data, your script **must** use parallel processing (e.g., multiprocessing, Dask, or parallel threads) to read and process the files simultaneously.

The processing pipeline must do the following:
1. **Clean and Normalize**: 
   - Strip leading and trailing whitespace from `server_id` and convert it to strictly uppercase.
   - Remove any exact duplicate rows within each file.
   - Drop any rows where *all* metric columns (`cpu_node1`, `mem_node1`, `cpu_node2`, `mem_node2`) are missing. Treat empty strings and `"NaN"` as missing. Fill remaining missing values with `0.0`.
2. **Reshape**: Convert the data from wide to long format. The new columns should be:
   `timestamp, server_id, node_id, metric, value`
   (e.g., a value in `cpu_node1` becomes `node_id = 'node1'`, `metric = 'cpu'`, and `value = [the numeric value]`).
3. **Aggregate**: Calculate the mean `value` across all timestamps for each unique combination of `server_id`, `node_id`, and `metric`. Round the mean to exactly 2 decimal places.
4. **Output**: Save the aggregated results to `/home/user/telemetry_summary.csv`.

The output CSV must have exactly these columns:
`server_id,node_id,metric,average_value`
The rows must be sorted alphabetically by `server_id`, then `node_id`, then `metric`.

Ensure your script is self-contained and handles the I/O cleanly. Run your script to generate the final output file.