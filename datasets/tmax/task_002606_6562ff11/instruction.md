You are a log analyst investigating thermal throttling issues on a cluster. 

There is a raw log file located at `/opt/data/server_logs.txt` on your local system. 
This log contains interleaved events from multiple nodes. The format of the log lines looks like this:
`[YYYY-MM-DD HH:MM:SS] LEVEL - NODE_NAME - T:TEMPERATURE L:LOAD`

For example:
`[2023-10-01 10:00:00] INFO - alpha - T:45.0 L:1.2`

Unfortunately, the temperature sensors on node `omega` occasionally fail and output `MISSING` instead of a float value. 

Your task is to:
1. Extract all log entries corresponding to the node `omega`.
2. Parse the unstructured text to extract the `timestamp`, `temperature` (T), and `load` (L).
3. For any `MISSING` temperature values, impute them using **time-based linear interpolation**. You can assume the temperature changes linearly over time between the nearest known valid readings before and after the missing data.
4. Save the cleaned and imputed data for node `omega` as a CSV file at `/home/user/omega_imputed.csv`.

The output CSV must have exactly this header:
`timestamp,temperature,load`

Requirements for the output:
- `timestamp` must be exactly as it appears in the log (e.g., `2023-10-01 10:00:00`).
- `temperature` must be rounded to exactly 2 decimal places (e.g., `46.00`, `51.50`).
- `load` should be written exactly as parsed (it will always be a valid float in the logs).
- Only include rows for node `omega`. Order the rows chronologically (which matches the log's order).
- You may use Python and any standard data science libraries (like `pandas`) available in the environment to accomplish this.