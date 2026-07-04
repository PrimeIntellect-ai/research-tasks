You are an automation specialist tasked with creating a data preprocessing workflow. You have received a raw log file from a legacy sensor network at `/home/user/raw_sensors.jsonl`. 

This file is in a JSON-lines format, but it has a problem: the legacy system occasionally writes malformed unicode escape sequences in the "note" field (specifically, an escaped `\uX` followed by exactly three digits, e.g., `\uX123`), which breaks standard JSON parsers like `jq` or Python's `json` module.

Your task is to write a Bash workflow (using any standard Linux command-line tools like `sed`, `awk`, `jq`, etc.) to process this file and output a clean, normalized CSV file at `/home/user/normalized_sensors.csv`.

Here are the specific requirements for the data transformation:
1. **Clean the Data**: Remove any occurrence of the malformed escape sequence (`\uX` followed by 3 digits) from the file before attempting to parse the JSON.
2. **Timestamp Alignment**: Extract the `time` field and round it down to the top of the hour. For example, `2023-10-12T08:14:05Z` should be aligned to `2023-10-12T08:00:00Z`.
3. **Wide-to-Long Reshaping**: The JSON objects contain both `temp` and `humidity` keys (wide format). You must reshape this into a long format. For each input row, generate two output rows: one for `temp` and one for `humidity`.
4. **Output Format**: The final file at `/home/user/normalized_sensors.csv` must be a comma-separated values file with the exact header: `time,device,metric,value`.
5. **Sorting**: Sort the final CSV data (excluding the header) alphabetically by `time`, then `device`, then `metric`.

Do not write a Python or Node.js script; use Bash and standard Unix text processing utilities. Ensure the output is saved exactly at `/home/user/normalized_sensors.csv`.