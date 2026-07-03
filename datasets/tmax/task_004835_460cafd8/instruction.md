I need your help setting up a data pipeline to track configuration changes over time. 

I have a log file at `/home/user/config_changes.log` that records system configuration changes. A legacy script was trying to convert this log into a time-series CSV, but it was silently dropping log entries that contained embedded newlines in their values or keys.

Your task is to write a Python script `/home/user/extract_ts.py` that correctly parses this log file and schedules it to run automatically.

Here are the requirements:
1. **Extraction**: Parse `/home/user/config_changes.log`. A new log entry always starts with a timestamp enclosed in brackets, e.g., `[YYYY-MM-DDThh:mm:ssZ]`. The format of an entry is:
   `[{timestamp}] USER: {user} KEY: {key} VALUE: {value}`
   Note that the `{key}` and `{value}` fields might contain literal newline characters. You must capture the entirety of the key and value up to the start of the next log entry (or the end of the file).
2. **Normalization**: 
   - Extract the `timestamp`, `key`, and `value`.
   - Normalize the `key` by: stripping leading/trailing whitespace, converting it to entirely lowercase, and replacing any sequence of whitespace characters (spaces, tabs, newlines) with a single underscore (`_`).
   - Strip leading/trailing whitespace from the `value`.
3. **Output**: Write the extracted data to `/home/user/config_ts.csv` using the standard CSV format (include headers: `timestamp,normalized_key,value`). Ensure that values with embedded newlines are properly quoted in the CSV.
4. **Scheduling**: Create a crontab entry for the current user to run this script every 15 minutes. 

You do not need to wait for cron to run; simply ensure the script works, run it once manually to generate `/home/user/config_ts.csv`, and then install the crontab.