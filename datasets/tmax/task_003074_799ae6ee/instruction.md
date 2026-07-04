You are an automation specialist setting up a data processing workflow. You have been given a messy log file containing system events from various legacy systems. The timestamps are inconsistent, and there are duplicate events recorded in different formats.

Your task is to write a Bash script at `/home/user/process_logs.sh` that processes `/home/user/events.txt` and outputs a cleaned, normalized, and deduplicated CSV file to `/home/user/normalized.csv`.

The input file `/home/user/events.txt` contains lines formatted as:
`[TIMESTAMP] | [LEVEL] | [MESSAGE]`

The `[TIMESTAMP]` can be in one of three formats (all representing UTC times):
1. `YYYY-MM-DD HH:MM:SS` (e.g., 2023-11-01 10:00:00)
2. `MM/DD/YYYY HH:MM:SS` (e.g., 11/01/2023 10:00:00)
3. Epoch timestamp (e.g., 1698832800)

Your script must:
1. Parse the log lines and extract the timestamp, level, and message.
2. Normalize all timestamps to Epoch seconds (integer). Assume all human-readable dates are in UTC.
3. Strip any leading/trailing whitespace from the extracted fields.
4. Deduplicate the records. If multiple records have the exact same Epoch timestamp, LEVEL, and MESSAGE, only keep one.
5. Sort the final records chronologically by the Epoch timestamp.
6. Write the output to `/home/user/normalized.csv` with the header: `timestamp,level,message`. 
7. Ensure the script has executable permissions and executes successfully.

Do not use external scripting languages like Python or Perl inside your bash script. Use standard Unix utilities (e.g., bash, awk, sed, date, sort, uniq).