You are a localization engineer for a global SaaS application. Users have been reporting missing translations (showing raw localization keys instead of translated text). The server logs every time a missing translation key is rendered. 

Your task is to write a Python script that processes these error logs to identify the highest priority missing translations over time, allowing the translation team to focus on the most impactful fixes first.

Write a Python script at `/home/user/process_loc_logs.py` that does the following:
1. Reads the log file located at `/home/user/loc_errors.jsonl`. Each line is a JSON object with fields: `timestamp` (ISO 8601 string, e.g., "2023-10-15T14:23:01Z"), `event` (always "MISSING_LOC"), `key` (the missing localization key), and `locale` (e.g., "es-ES").
2. Parses the timestamps and aligns them into 1-hour tumbling windows (e.g., a timestamp of `2023-10-15T14:23:01Z` falls into the `2023-10-15T14:00:00Z` window).
3. For each 1-hour window, aggregates the count of missing occurrences for each unique `locale` and `key` combination.
4. Identifies the **single most frequent** missing `locale` and `key` combination for each 1-hour window. If there is a tie for the highest count in a window, resolve it by selecting the combination that comes first alphabetically by `locale`, then by `key`.
5. Outputs the results to a CSV file at `/home/user/top_missing.csv` with the exact header: `window_start,locale,key,error_count`.
6. The CSV must be sorted chronologically by `window_start`.

After writing the script, execute it to generate the `/home/user/top_missing.csv` file.