You are tasked with analyzing logs from a configuration manager to identify bad configuration pushes that caused sudden spikes in system load.

In the directory `/home/user/config_logs/`, there are several log files named `server_<id>.log`. Each line in these logs records a configuration check and the current system load, but the logs are messy and have missing entries.

The log lines generally follow this format (though there might be slight spacing variations):
`[YYYY-MM-DD HH:MM:SS] Config sync complete. current_load=<value>`

However, the logging system often drops messages, resulting in gaps of several minutes between entries. 

Your objective is to write and execute a Python script that does the following:
1. **Parallel Processing:** Read and process the log files in parallel.
2. **Parsing:** Use Regex to extract the timestamp and the `current_load` float value from each line.
3. **Resampling & Gap-filling:** For each server, create a minute-by-minute time series from its earliest to its latest timestamp. Fill any missing minutes using "forward-fill" (i.e., carry over the last known `current_load` value to the missing minutes).
4. **Anomaly Detection:** An anomaly is defined as a minute-to-minute increase in `current_load` of **strictly greater than 45.0** (calculated after gap-filling).
5. **Output:** Save the detected anomalies to a CSV file at `/home/user/anomalies.csv`. 

The output CSV must have exactly this header: `Timestamp,Server,Increase`
The `Timestamp` must be formatted as `YYYY-MM-DD HH:MM:00`.
The `Server` is the filename without the `.log` extension (e.g., `server_1`).
The `Increase` should be the float value of the load increase rounded to 1 decimal place.
Sort the final CSV by Timestamp ascending, then by Server ascending.

Write the Python script, run it, and ensure `/home/user/anomalies.csv` is correctly generated.