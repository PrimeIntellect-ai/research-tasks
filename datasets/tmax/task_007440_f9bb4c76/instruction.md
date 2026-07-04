You are tasked with analyzing tracking logs from a configuration manager. The logs are stored in two JSON-lines files from two different application subsystems.

Your goal is to parse these files, clean encoding errors, merge them, compute a rolling statistic, and output the results as a CSV file.

The input files are located at:
- `/home/user/data/app1_configs.jsonl`
- `/home/user/data/app2_configs.jsonl`

**Requirements:**
1. **Character Encoding Handling:** Standard JSON parsers break on these files because some string values contain malformed unicode escape sequences (e.g., literal `\u` followed by characters that do not form a valid 4-digit hexadecimal code, like `\u12G4` or `\uXXYZ`). 
   Before parsing each line as JSON, you must find any literal occurrence of `\u` followed by exactly 4 characters that are *not* a valid hex sequence, and replace that entire 6-character sequence with the exact string `[INVALID]`. (Valid `\uXXXX` sequences should be left alone for the JSON parser to handle).
2. **Merge and Sort:** Combine the parsed records from both files and sort them chronologically by the `timestamp` field (ascending).
3. **Rolling Statistics:** Calculate a 3-event rolling average of the `memory_limit_mb` field. The window size is exactly 3 events (the current event and the up to 2 preceding events in the sorted merged list).
4. **Output:** Write the results to `/home/user/output/rolling_configs.csv`. 
   The CSV must have the following header: `timestamp,app_id,memory_limit_mb,rolling_avg_memory`.
   The `rolling_avg_memory` values must be formatted to exactly 2 decimal places (e.g., `100.00`, `266.67`).

Write and execute a Python script to perform this data processing pipeline. Ensure `/home/user/output/` exists before writing the file.