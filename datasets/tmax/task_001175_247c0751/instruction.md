You are tasked with building a configuration management and data sampling service.

We have a legacy workflow where system administrators leave audio memos for configuration updates. You have been provided with an audio file at `/app/sysadmin_memo.wav`. 
You must transcribe this audio file to find the required configuration updates. The memo will specify changes to three specific configuration keys: `maintenance_mode` (boolean), `max_workers` (integer), and `target_region` (string).

We also have a base configuration file at `/app/initial_config.json` containing default values.
And we have a large log dataset at `/app/server_logs.csv` with columns: `request_id`, `timestamp`, `status_code`, `response_time`.

Your objective is to:
1. Transcribe the audio file to extract the three configuration values.
2. Merge these extracted values with the base configuration (overriding the defaults).
3. Save the merged configuration to `/home/user/current_config.json`.
4. Append an entry to a pipeline log file at `/home/user/config_audit.log` documenting the change. The log format must be exactly: `[<TIMESTAMP>] CONFIG_UPDATED: maintenance_mode=<val>, max_workers=<val>, target_region=<val>` (use ISO 8601 format for the timestamp).
5. Write and start an HTTP server listening on `127.0.0.1:9090` that performs the following:
    - **GET `/config`**: Returns the current configuration as a JSON payload.
    - **POST `/config`**: Accepts a JSON payload to update the configuration. 
        - It must require an Authorization header: `Bearer admin-token-2024`.
        - It must perform constraint-based validation: `max_workers` must be an integer between 1 and 100, and `target_region` must be a string starting with `eu-` or `us-`. If validation fails, return a 400 status code.
        - Upon success, update the configuration, append to `/home/user/config_audit.log`, and return a 200 status code.
    - **GET `/sample`**: Reads `/app/server_logs.csv` and returns a stratified sample of the data based on the current configuration. It must return a JSON object where keys are the unique `status_code` values, and the value is a list of exactly `max_workers` sampled rows for that status code. The rows must be sampled randomly but deterministically (if possible) or just validly stratified. If a stratum has fewer than `max_workers` rows, include all available rows for that stratum.

Your server must be robust and continue running in the background. Do not exit the server once it is started.