You are tasked with fixing a data processing pipeline for a configuration management system. An ETL job extracts configuration change events from our servers, but due to a retry bug, the log file contains duplicate records.

We need a C++ application that cleans this data, joins it with server metadata, and produces an hourly aggregated report of configuration changes by environment.

Here is the setup:
1. You have a log file at `/home/user/data/config_logs.txt`. The log lines look like this:
   `[2023-10-24T08:15:32Z] INFO: Server {srv-001} updated config [max_connections] -> 500`
2. You have a server metadata file at `/home/user/data/server_meta.csv` in the format:
   `ServerID,Role,Environment`

Your objective is to write a C++ program at `/home/user/src/aggregator.cpp` that performs the following:

1. **Parse:** Read `/home/user/data/config_logs.txt`. Use C++ standard regex to extract the Timestamp (ISO 8601), ServerID, ConfigKey, and NewValue from each line.
2. **Deduplicate:** The ETL job sometimes retries and writes the exact same log entry multiple times. Remove exact duplicates (records having the exact same Timestamp, ServerID, ConfigKey, and NewValue).
3. **Join:** Read `/home/user/data/server_meta.csv` and join the parsed log records with the server metadata using the `ServerID`. If a ServerID is not found in the CSV, ignore the log record.
4. **Time-Based Bucketing:** Truncate the timestamps to the start of the hour. For example, `2023-10-24T08:15:32Z` becomes `2023-10-24T08:00:00Z`.
5. **Aggregate:** Count the number of unique configuration changes per Hour per Environment.
6. **Output:** Write the results to `/home/user/output/hourly_summary.json` as a JSON array of objects, sorted chronologically by hour, and then alphabetically by environment.

The output JSON must strictly follow this structure and use 4 spaces for indentation:
```json
[
    {
        "change_count": 2,
        "environment": "Production",
        "hour": "2023-10-24T08:00:00Z"
    }
]
```

**Requirements:**
- Your C++ code must be self-contained in `/home/user/src/aggregator.cpp`.
- You may install any necessary C++ packages (like `nlohmann-json3-dev`) via `apt-get` using `sudo` (you have passwordless sudo).
- Compile your code using `g++ -std=c++17 /home/user/src/aggregator.cpp -o /home/user/bin/aggregator`.
- Run your binary to generate the output file at `/home/user/output/hourly_summary.json`.
- Do not modify the original data files.