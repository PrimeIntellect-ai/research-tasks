I need you to write a Bash-based data processing pipeline to clean, anonymize, and summarize a corrupted JSON-lines dataset. 

As a data scientist, I was handed a raw events log located at `/home/user/raw_events.jsonl`. Unfortunately, the system that generated this file had a bug. Some lines contain broken unicode escape sequences that cause standard JSON parsers (like `jq`) to fail, and there are duplicate events.

Write a Bash script at `/home/user/process_data.sh` that performs the following steps in order:

1. **Cleaning & Normalization:**
   - Read `/home/user/raw_events.jsonl`.
   - Some JSON lines are corrupted by an invalid unicode escape sequence literal: `\uZZZZ`. Use standard text processing tools (`sed`, `awk`, etc.) to replace all occurrences of the literal string `\uZZZZ` with `[REDACTED]` before trying to parse the JSON.
   - Discard any lines that are still invalid JSON (i.e., lines that `jq` cannot parse even after the above fix).

2. **Anonymization / Masking:**
   - For all valid JSON records, mask the `email` field. Replace the local part of the email (everything before the `@`) with exactly three asterisks `***`. For example, `alice.smith@example.com` must become `***@example.com`. 
   - If a record does not have an `email` field or the field is null, leave it as is.

3. **Deduplication:**
   - Deduplicate the valid records based on the `event_id` field.
   - If multiple records share the same `event_id`, keep *only* the record with the oldest (earliest) `timestamp`. The `timestamp` is in standard ISO-8601 format, so lexicographical sorting is sufficient.

4. **Output & Archiving (Local-Remote Simulation):**
   - Save the final, cleaned, anonymized, and deduplicated JSON-lines to `/home/user/cleaned_data.jsonl`.
   - Compress this file using `gzip` and copy it to the archive directory `/home/user/archive/` (create this directory if it doesn't exist). Name the archived file `cleaned_data.jsonl.gz`.

5. **Aggregation / Summary Statistics:**
   - Generate a CSV file at `/home/user/summary.csv` that contains the count of each `event_type` present in the *final deduplicated* dataset.
   - The CSV must have exactly this header: `event_type,count`
   - The rows must be sorted alphabetically by `event_type`.

6. **Pipeline Logging:**
   - Your script must write a log file to `/home/user/pipeline.log` containing exactly these three lines, populated with the correct integer counts:
     `Total raw lines: <number>`
     `Valid parsed lines: <number>`
     `Final deduplicated lines: <number>`

Make sure your script `/home/user/process_data.sh` is executable and run it to produce the required output files. You may install `jq` if it is not already installed.