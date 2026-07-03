You are tasked with building a robust configuration change tracking pipeline in Bash. We have several servers that dump their configuration state periodically into JSON-Lines (`.jsonl`) files. These files contain raw configuration strings, some of which include Unicode escape sequences (e.g., `\u0048\u0065\u006c\u006c\u006f`) that represent the actual configuration content.

Write a Bash script at `/home/user/process_configs.sh` that performs the following steps:

1. **Parallel Processing & Extraction:** Find all `.jsonl` files in `/home/user/config_dumps/`. Process them in parallel (using at least 2 concurrent processes) to extract the `server_id`, `timestamp`, and `config_data` from each JSON object. You must correctly parse the Unicode escape sequences in `config_data` into actual UTF-8 strings.
2. **Hash-based Deduplication:** Calculate the SHA-256 hash of the decoded `config_data`. If multiple entries across any servers have the exact same configuration data, keep only the entry with the chronologically earliest `timestamp`.
3. **Database Bulk Import:** Import the deduplicated records into an SQLite3 database located at `/home/user/config_inventory.db`. Create a table named `configs` with the schema: `hash TEXT PRIMARY KEY, server_id TEXT, timestamp TEXT, data TEXT`.
4. **Summary Statistics:** Generate a CSV file at `/home/user/stats.csv` that contains the aggregation of the raw data. It must have the header `hash,server_count` and list each unique configuration hash alongside the total number of times that exact configuration appeared across *all* input lines (before deduplication), sorted by `server_count` descending, then by `hash` ascending.
5. **Scheduling:** Add a cron job for the `user` that schedules `/home/user/process_configs.sh` to run exactly at the top of every hour (minute 0).

Ensure your script is executable. The input JSON files have the format:
`{"server_id": "srv1", "timestamp": "2023-10-01T10:00:00Z", "config_data": "port=80\\nmode=\\u0061\\u0063\\u0074\\u0069\\u0076\\u0065"}`

You may install any standard package (e.g., `jq`, `sqlite3`, `parallel`) using `sudo apt-get` if needed, but your final script must not require interactive `sudo` prompts. Run the script once manually to populate the database and stats file so your work can be verified.