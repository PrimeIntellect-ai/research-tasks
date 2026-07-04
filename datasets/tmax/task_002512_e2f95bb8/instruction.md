You are an analyst investigating a flaky ETL pipeline that processes multi-lingual data. When the pipeline encounters transient errors, it retries, resulting in duplicate log entries. Because of different text encoding paths during retries, the duplicate messages often use different Unicode normalization forms or casing, making standard deduplication fail.

You have a raw log file located at `/home/user/etl_logs.txt`. 

Each line in the log file follows this exact format:
`[YYYY-MM-DDThh:mm:ssZ] LEVEL JOB_ID - Message text`

Your task is to write and execute a Python script that processes this log file and generates a cleaned, deduplicated JSON Lines (JSONL) file at `/home/user/cleaned_logs.jsonl`.

Here are the specific requirements for your processing pipeline:

1. **Extraction**: Parse each line to extract the timestamp, level, job_id, and message. Ignore any lines that do not strictly match the format (these act as validation checkpoints for malformed logs).
2. **Normalization**: 
   - Convert the extracted message text to Unicode **NFKC** normalization.
   - Convert the extracted message text to strictly **lowercase**.
   - Strip leading/trailing whitespace from the message.
3. **Windowed Deduplication**: 
   - The ETL pipeline retries within 5 minutes. You must filter out duplicate records.
   - A record is considered a duplicate if it has the same `job_id` AND the same **normalized** message as another record that occurred within a rolling **5-minute (300 seconds) window** prior to it. 
   - Keep the *first* occurrence of the record and discard subsequent duplicates within that 5-minute window.
   - Records with the same job_id and message that occur strictly more than 5 minutes (>= 301 seconds) apart should both be kept.
4. **Output**: Write the cleaned, unique records to `/home/user/cleaned_logs.jsonl`. Each line must be a valid JSON object with the following keys:
   - `"timestamp"` (string, exactly as it appeared in the input)
   - `"level"` (string)
   - `"job_id"` (string)
   - `"message"` (string, the normalized version)

Ensure your script processes the entire file and creates the exact output required.