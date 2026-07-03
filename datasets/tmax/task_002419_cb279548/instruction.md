You are a storage administrator managing a fleet of servers. A legacy logging daemon continuously writes disk usage telemetry to CSV files, which are frequently rotated by an aggressive log-rotation script. 

To audit disk usage without racing the active writer, you analyze the recently rotated log files. However, the files are massive, and standard file I/O is too slow for your auditing pipeline.

Your task is to write a highly efficient C program that parses a JSON configuration file for disk thresholds, uses memory-mapped I/O (`mmap`) to read the rotated CSV logs, and outputs threshold violations.

**Requirements:**
1. **Dependencies**: You may use external C libraries for JSON parsing (e.g., `libjansson-dev` or `libcjson-dev`). You will need to install them.
2. **C Program Requirements**:
   - Create your source code at `/home/user/analyze.c`.
   - The program must take command-line arguments: the path to the JSON config file, followed by one or more paths to CSV log files.
     Usage: `./analyze <config.json> <log1.csv> [log2.csv ...]`
   - **JSON Configuration Parsing**: The JSON file contains key-value pairs where the key is the mount point (string) and the value is the maximum allowed usage in MB (integer).
   - **CSV Parsing via `mmap`**: The program **must** use `mmap` to read the CSV files. Standard `fopen`/`fread`/`fgets` is strictly forbidden for reading the CSV files.
   - The CSV files have the format: `timestamp,mount_point,usage_mb` (no header row).
     Example: `2023-10-25 14:00:00,/var/log,850`
   - **Output**: The program should write to `stdout`. For every record in the CSV that strictly exceeds (> not >=) the threshold defined in the JSON for that mount point, output a line in exactly this format:
     `[<timestamp>] ALERT: <mount_point> exceeded threshold (Current: <usage_mb> MB, Limit: <limit_mb> MB)`
3. **Execution & Redirection**:
   - Compile your program to `/home/user/analyze`.
   - Run your program against the configuration file `/home/user/thresholds.json` and all CSV files in `/home/user/logs/` (passed via shell globbing like `/home/user/logs/*.csv`).
   - Redirect the standard output of your program to `/home/user/alerts.log`.

**Files provided in the environment:**
- `/home/user/thresholds.json` (The configuration)
- `/home/user/logs/` (Directory containing multiple `.csv` files)

Ensure your program handles missing configuration keys gracefully (if a mount point is in the CSV but not the JSON, ignore it). Build, test, and execute the final command to generate `/home/user/alerts.log`.