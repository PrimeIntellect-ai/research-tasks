You are tasked with building a configuration management data pipeline. You have a system that dumps raw server configuration state files as JSONs into `/home/user/raw_configs/`. Your goal is to normalize these configurations, bulk load them into a relational database, and generate summary statistics about the infrastructure over time.

Please write and execute a Python script (`/home/user/process_configs.py`) that performs the following steps:

1. **Normalization**: Read all JSON files in `/home/user/raw_configs/`. Each file contains a nested JSON object representing a server's state at a specific timestamp.
   Example structure:
   ```json
   {
     "server_id": "srv-alpha",
     "timestamp": 1682001000,
     "hardware": {
       "ram_gb": 16,
       "cpu_cores": 4
     },
     "software": {
       "os": "ubuntu-22.04",
       "is_active": "true"
     }
   }
   ```
   You must flatten this structure so nested keys are joined by an underscore (e.g., `hardware_ram_gb`, `software_os`). Additionally, standardize the `is_active` boolean: if it is the string `"true"` or `"false"`, convert it to the integer `1` or `0` respectively.

2. **Bulk Import**: Create a SQLite database at `/home/user/config_history.db`. Create a table named `server_configs` with the following schema:
   - `server_id` (TEXT)
   - `timestamp` (INTEGER)
   - `hardware_ram_gb` (INTEGER)
   - `hardware_cpu_cores` (INTEGER)
   - `software_os` (TEXT)
   - `software_is_active` (INTEGER)
   
   Bulk insert all normalized configuration records into this table.

3. **Summary Statistics**: Query the SQLite database to generate a summary report. For each `server_id`, calculate:
   - `snapshot_count`: The total number of configuration states recorded.
   - `max_ram_gb`: The maximum `hardware_ram_gb` ever recorded for this server.
   - `active_snapshots`: The number of snapshots where `software_is_active` was `1`.

4. **Export**: Export these summary statistics to a CSV file at `/home/user/config_summary.csv`. The CSV must have headers exactly matching the calculated fields: `server_id,snapshot_count,max_ram_gb,active_snapshots`. The rows must be sorted alphabetically by `server_id`.

Ensure your script handles all files in the directory and produces the exact output format requested.