You are a localization engineer at a global software company. You need to process a batch of raw user feedback logs to help prioritize translation updates. The feedback contains sensitive user data that must be anonymized, and it needs to be aggregated by language and time to see when specific languages spike in activity.

Your task is to write a Python script at `/home/user/process_feedback.py` that implements a mini-ETL pipeline with strict validation, masking, bucketing, and logging.

### Input Data
There is a raw JSONL (JSON Lines) file located at `/home/user/raw_feedback.jsonl`.
Each line is a JSON object that may contain the following fields:
- `id`: (string) Unique identifier.
- `timestamp`: (string) ISO 8601 format (e.g., "2023-10-25T14:32:10Z").
- `user_email`: (string) Optional email address.
- `ip_address`: (string) Optional IPv4 address.
- `text`: (string) The feedback text.
- `lang`: (string) Language code (e.g., "en", "es", "fr").

### Pipeline Requirements

Your script must execute the following logical phases in order, acting as a simple DAG:

1. **Validation Checkpoint (Quality Gate):**
   - Read the input file. 
   - A valid record MUST contain a non-empty `timestamp`, `text`, and `lang`.
   - If a record is missing any of these three fields, or if they are null/empty, it must be dropped.

2. **Data Masking and Anonymization:**
   - For valid records, anonymize the `user_email` field: keep the first letter, replace the rest of the local part with `***`, and keep the domain. (e.g., `alice@example.com` becomes `a***@example.com`). If `user_email` is missing, do nothing.
   - Anonymize the `ip_address` field: replace the entire IP address with the exact string `[IP_REDACTED]`. If missing, do nothing.
   - Save these valid, anonymized records as a JSONL file at `/home/user/processed/anonymized_feedback.jsonl`.

3. **Time-Based Bucketing and Aggregation:**
   - Parse the `timestamp` of the valid records and bucket them by hour (e.g., "2023-10-25T14:32:10Z" becomes "2023-10-25T14:00:00Z").
   - Count the number of feedback entries per `lang` per hourly bucket.
   - Save this aggregation as a CSV file at `/home/user/processed/hourly_lang_summary.csv` with exactly three columns: `hour_bucket`, `lang`, `feedback_count`. The CSV must include a header row.

4. **Pipeline Logging and Monitoring:**
   - Throughout the process, append structured text logs to `/home/user/logs/pipeline.log`.
   - The log file MUST contain the following exact phrases (where `<X>` is the correct integer):
     - `INFO: Pipeline started`
     - `WARNING: Dropped <X> records due to validation failures`
     - `INFO: Anonymized <X> valid records`
     - `INFO: Pipeline complete`

### Execution
- Ensure you create the `/home/user/processed` and `/home/user/logs` directories before writing to them.
- Run your script to generate the outputs.