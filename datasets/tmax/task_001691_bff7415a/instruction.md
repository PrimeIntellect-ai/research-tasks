You are tasked with building a configuration management tracking script in Bash. You have a system that stores its configuration across multiple file formats, and a historical log of all configuration changes. We need to analyze this log to track how frequently our current configuration keys are being updated on a monthly basis.

Create a Bash script at `/home/user/tracker.sh` that performs the following operations:

1. **Multi-format File Reading & Key Extraction**
   Read the current configuration files located in `/home/user/configs/` and extract all their configuration keys:
   - `/home/user/configs/settings.json`: A nested JSON file. Extract all paths to scalar values, joined by dots (e.g., `database.connection.port`).
   - `/home/user/configs/system.xml`: An XML file. Extract all leaf node paths, joined by dots (e.g., `system.network.timeout`).
   - `/home/user/configs/env.csv`: A CSV file with headers `key,value`. Extract all values from the `key` column.

2. **Tokenization and Normalization**
   Normalize all extracted keys by:
   - Converting them entirely to lowercase.
   - Replacing any dots (`.`) with underscores (`_`).
   - Removing any leading or trailing whitespace.
   This represents the "Active Keys" set.

3. **Windowed Aggregation of Historical Changes**
   Read the changelog file at `/home/user/data/history.log`. The file has space-separated columns in the following format:
   `YYYY-MM-DD HH:MM:SS [Filename] [RawKey] [Action]`
   Example: `2023-10-05 14:32:01 [settings.json] [database.connection.port] [UPDATE]`
   
   - Filter the log for rows where the Action is exactly `[UPDATE]`.
   - Normalize the `[RawKey]` using the exact same normalization rules as step 2.
   - Group the data by normalized key and by month (format: `YYYY-MM`).
   - Calculate the total number of updates per month for each key.

4. **Filtering and Output**
   - Retain only the aggregated log data for keys that are *currently present* in the "Active Keys" set derived from the config files in Step 1. Ignore updates for deprecated keys that no longer exist in the current configs.
   - Output the final aggregated data as a JSON file at `/home/user/output/aggregated_changes.json`.
   - The JSON structure must be a dictionary where the top-level keys are the normalized configuration keys, and their values are dictionaries mapping the month (`YYYY-MM`) to the integer count of updates. Do not include months with 0 updates.

Example Expected Output Format:
```json
{
  "database_connection_port": {
    "2023-09": 3,
    "2023-10": 1
  },
  "system_network_timeout": {
    "2023-10": 5
  }
}
```

Constraints & Requirements:
- You must write the solution primarily in Bash (using standard UNIX utilities like `awk`, `sed`, `grep`, `jq`, `xmlstarlet`, etc.).
- Ensure your script creates the `/home/user/output/` directory if it does not exist.
- Run your script once it is written so the output file `/home/user/output/aggregated_changes.json` is generated for verification.
- You have `sudo` privileges to install any missing tools (like `jq` or `xmlstarlet`) if needed.