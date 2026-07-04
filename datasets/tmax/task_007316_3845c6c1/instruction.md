You are tasked with fixing a broken data pipeline for our configuration management system. 

The system continuously exports server state changes to a JSON-lines file at `/home/user/data/config_changes.jsonl`. However, a bug in the upstream logger sometimes emits malformed unicode escape sequences (e.g., `\uZZZZ` or `\uXX99`) in the `note` field. Standard JSON parsers crash when trying to read these lines.

Write a script (in any language you prefer) to process this file. Since the production files are massive, your script must stream the file line-by-line rather than loading the entire file into memory at once.

Your processing script must perform the following tasks:
1. **Sanitize the input:** Intercept the raw string of each line and remove any invalid unicode escape sequences (specifically, any occurrence of `\u` followed by 4 characters where at least one character is not a valid hexadecimal digit `[0-9a-fA-F]`). Replace the invalid 6-character sequence (e.g., `\uZZZZ`) with `?`.
2. **Reshape the data:** The valid JSON lines have a wide format: `{"ts": <int>, "states": {"<server_name>": {"load": <float>, "mem": <float>}, ...}, "note": "..."}`. Flatten this into a long format containing `ts`, `server`, and `load`.
3. **Windowed Aggregation:** For each `server`, compute a 2-period rolling average of the `load` metric, ordered by `ts`. If it is the first record for a server, the rolling average is just that record's load. 
4. **Output:** Write the results to a CSV file at `/home/user/output/rolling_loads.csv` with the headers `ts,server,rolling_load`. Round `rolling_load` to 1 decimal place. The rows must be sorted by `ts` ascending, then `server` name alphabetically.

Finally, write a bash script at `/home/user/setup_cron.sh` that, when executed, adds a crontab entry to run a script named `/home/user/process.sh` (you can wrap your main code in this) at exactly minute 0 of every hour.

Constraints:
* The input file exists at `/home/user/data/config_changes.jsonl`.
* The output directory `/home/user/output/` already exists.
* Ensure you create `/home/user/process.sh` and `/home/user/setup_cron.sh`, and make them executable.