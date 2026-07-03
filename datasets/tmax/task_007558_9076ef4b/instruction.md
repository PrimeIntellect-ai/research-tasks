You are helping a researcher organize their experimental dataset. You have been given a large, multi-line log file of experimental runs located at `/home/user/experiments.log`. 

Your task is to parse this log file, extract the relevant data, anonymize it, and convert it into a structured JSONL (JSON Lines) format. You must write a Python script at `/home/user/process_logs.py` to accomplish this, and then execute it to produce the final output at `/home/user/structured_runs.jsonl`.

The input log file contains multiple records. Each record follows this exact structure:
```
--- BEGIN RUN ---
Timestamp: <ISO-8601 string>
RunID: <integer>
User: <username>
Parameters:
<multi-line parameter string, can be indented>
Results: <string>
--- END RUN ---
```
Note that the `Parameters:` section can span multiple lines until the `Results:` line is encountered.

You need to perform the following transformations for each run:
1. Parse the multi-line record into its constituent fields: `Timestamp`, `RunID`, `User`, `Parameters`, and `Results`.
2. **Anonymization**: Replace the value of the `User` field with the exact string `"USER_ANONYMIZED"`.
3. **Normalization**: For the `Parameters` field, strip any leading and trailing whitespace from *each line* of the parameters, and join them back together with a single newline character (`\n`). If the parameters section is empty, it should be an empty string.
4. Output the transformed record as a single JSON object per line in `/home/user/structured_runs.jsonl`. The keys in the JSON must exactly match the field names: `"Timestamp"`, `"RunID"`, `"User"`, `"Parameters"`, and `"Results"`.

Ensure your Python script cleanly handles the parsing, transformation, and formatting. After writing the script, run it so that the `/home/user/structured_runs.jsonl` file is generated.