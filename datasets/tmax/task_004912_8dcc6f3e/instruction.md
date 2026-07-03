You are an AI assistant acting as a configuration manager. We have a system that dumps its entire configuration state into an append-only log file whenever a service restarts, but to save space, the configurations are stored in a custom compressed format. 

Your task is to parse this log file, extract a specific configuration value over time, and generate a CSV report of its changes.

Here are the details:
1. The input log file is located at `/home/user/config_history.log`.
2. Each line in the log file represents a snapshot and is formatted as: `<UNIX_TIMESTAMP> <PAYLOAD>`
3. The `<PAYLOAD>` is a base64-encoded string. Once decoded from base64, it is a zlib-compressed payload. Once decompressed using zlib, it reveals a standard JSON string representing the system configuration.
4. The JSON configuration has a nested structure. You need to track the value of `max_connections` located under the `database` key (i.e., `database.max_connections`).
5. Write a Python script to process this file and output a CSV file at `/home/user/connection_changes.csv`.
6. The CSV must have the header: `timestamp,old_value,new_value`
7. The CSV should only contain rows for timestamps where the `database.max_connections` value **changed** from the previously seen valid configuration snapshot. The first snapshot establishes the baseline value and should *not* be recorded in the CSV as a change. 
8. The CSV should be sorted chronologically (which matches the order of the input log file).

Please write and execute the Python script to create `/home/user/connection_changes.csv`.