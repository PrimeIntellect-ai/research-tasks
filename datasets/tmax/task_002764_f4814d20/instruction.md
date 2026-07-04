As an automation specialist, you are tasked with creating a robust data processing pipeline to handle a large, malformed log export from one of our legacy systems.

The logs are stored in a JSON-Lines file located at `/home/user/data/logs.jsonl`. Because this file can grow very large in production, your solution must stream the file line-by-line rather than loading the entire file into memory at once.

Unfortunately, the legacy system had a bug where it occasionally truncated messages in the middle of a Unicode escape sequence (e.g., leaving a dangling `\uD83` instead of a full `\uXXXX` sequence or valid surrogate pair) or emitted isolated surrogate halves. This causes standard JSON parsers to throw errors when reading these specific lines.

Your task is to write a Python script `/home/user/process_logs.py` that accomplishes the following:
1. **Stream** `/home/user/data/logs.jsonl` line by line.
2. **Character Encoding Repair**: Parse each JSON line. If a line contains invalid Unicode escape sequences that break the JSON parser, you must gracefully handle and repair it so that the invalid escape is effectively replaced or sanitized (for instance, substituting the broken escape with the Unicode Replacement Character `U+FFFD` or stripping it), allowing the JSON object to be fully parsed. *Do not just skip the broken lines!* Every line must be parsed and counted.
3. **Time-based Bucketing**: Extract the `ts` (timestamp) field, which is in ISO 8601 format (e.g., `2023-01-01T14:32:01Z`). Truncate the timestamp to the start of the hour (e.g., `2023-01-01T14:00:00Z`).
4. **Aggregation**: Count the number of events per `hour` and per `type` (event type).
5. **Output**: Write the aggregated results to a CSV file at `/home/user/summary.csv`. The CSV must have exactly three columns: `hour`, `type`, and `count`. Include a header row. 
   - The CSV must be sorted chronologically by `hour` (ascending), and then alphabetically by `type` (ascending) for ties within the same hour.

Ensure your Python script relies only on the Python standard library. Run your script to produce the final `summary.csv` file. 

Environment Setup:
- The `/home/user/data/` directory and the `logs.jsonl` file already exist.