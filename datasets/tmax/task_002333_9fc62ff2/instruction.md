You are an automation specialist tasked with building a robust ETL pipeline. Your team processes user data from various sources (CSV and JSONL formats) into a consolidated Parquet file. 

However, the pipeline often fails mid-execution and is automatically retried. Because the current naive approach simply appends data on retry, the resulting Parquet file is filled with duplicate records and stale data. Furthermore, privacy compliance requires masking Personally Identifiable Information (PII), but this has not been implemented.

Your task is to write a Python script `/home/user/etl_pipeline.py` that handles data ingestion, anonymization, deduplication, and persistence.

**Script Interface:**
The script must accept two positional arguments:
`python3 /home/user/etl_pipeline.py <input_file> <output_parquet>`
- `<input_file>`: Path to the incoming data file. This will be either a CSV file (with `.csv` extension) or a JSON Lines file (with `.jsonl` extension).
- `<output_parquet>`: Path to the target Parquet file.

**Requirements:**
1. **Multi-format Reading:** Read the incoming data based on its extension. Both formats contain the same columns/keys: `user_id` (integer), `name` (string), `email` (string), `phone` (string), and `timestamp` (ISO 8601 string).
2. **Stateful Consolidation:** If `<output_parquet>` already exists, read its contents and merge them with the new incoming data. If it doesn't exist, process only the new data.
3. **Deduplication:** To handle retries and updates, deduplicate the merged dataset by `user_id`. If multiple records exist for the same `user_id`, keep *only* the record with the most recent `timestamp`.
4. **Data Masking (Anonymization):**
   - **Email:** Mask the local part of the email (everything before the `@`) with exactly three asterisks `***`. (e.g., `jane.doe@example.com` becomes `***@example.com`).
   - **Phone:** Mask the last 4 characters of the phone number with `XXXX`. If the phone number is 4 characters or shorter, replace the entire string with `XXXX`. (e.g., `555-123-4567` becomes `555-123-XXXX`, and `911` becomes `XXXX`).
5. **Output:** Save the consolidated, deduplicated, and masked data back to `<output_parquet>`, overwriting the file.

**Data constraints:**
- You can use `pandas` and `pyarrow` or `fastparquet` as they are standard for this task.
- Ensure the output Parquet file retains the same schema (`user_id`, `name`, `email`, `phone`, `timestamp`).

You must create and test `/home/user/etl_pipeline.py`. To test your code, you can use the sample files located in `/home/user/data/`.