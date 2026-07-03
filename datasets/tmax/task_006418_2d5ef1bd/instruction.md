You are a data engineer building an ETL pipeline. You have been given a raw JSON-Lines file containing chat logs at `/home/user/raw_chat_logs.jsonl`. 

The upstream system that generates these logs has bugs, leading to inconsistent timestamps, missing minutes (gaps in the time series), unmasked PII, and occasional malformed unicode escape sequences that break standard JSON parsers.

Your task is to write a Python script (you can name it `/home/user/process_etl.py`) that reads `/home/user/raw_chat_logs.jsonl`, cleans the data, and writes the output to `/home/user/clean_logs.jsonl`.

Apply the following transformations and business logic in order:

1. **Robust JSON Parsing**: Some lines contain invalid unicode escape sequences (e.g., `\u` followed by non-hex characters like `\u00ZZ`). If a line contains invalid unicode escapes, remove the invalid sequence entirely (e.g., `\u00ZZ` becomes an empty string) *before* parsing it with a JSON library.
2. **Timestamp Alignment**: The `ts` field comes in three formats:
   - ISO-8601 strings (e.g., `"2023-05-12T14:00:00Z"`)
   - US Date-Time strings (e.g., `"05/12/2023 14:01:00"`) - Assume UTC.
   - Unix epoch integers (e.g., `1683900180`) - Assume UTC.
   Convert all parsed timestamps to a standard ISO-8601 UTC string format: `YYYY-MM-DDTHH:MM:SSZ`.
3. **Data Masking**: Find any email addresses in the `message` field and replace them completely with the exact string `***@***.***`. (Assume standard email formats).
4. **Text Normalization**: Convert the `message` text to lowercase and strip leading and trailing whitespace.
5. **Interpolation/Imputation**: The data should have exactly one record per minute between the earliest and latest timestamps in the dataset. Detect any missing minutes and insert an imputed record. Imputed records must have:
   - `ts`: the missing minute timestamp in ISO-8601 UTC format.
   - `user_id`: `"unknown"`
   - `message`: `"imputed"`
6. **Sorting**: The final output in `/home/user/clean_logs.jsonl` must be sorted chronologically by the `ts` field.

Ensure your Python script creates the output file at exactly `/home/user/clean_logs.jsonl`. You can run your script in the terminal to process the file.