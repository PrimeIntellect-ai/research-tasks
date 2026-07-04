You are an automation specialist tasked with building a robust, idempotent ETL pipeline. An upstream system regularly retries data deliveries, resulting in duplicated transaction records scattered across multiple file formats.

Your objective is to write a Python script `/home/user/etl/etl_pipeline.py` that reads these files, deduplicates the records using a hash-based fingerprint, logs the pipeline's progress, and writes a unified output.

### 1. Input Data
You will find three input files in `/home/user/etl/input/`:
*   `batch_a.csv` (CSV format)
*   `batch_b.json` (JSON format, array of objects)
*   `batch_c.xml` (XML format, `<transactions><transaction>...</transaction></transactions>`)

Every record across all formats contains the following logical fields:
*   `delivery_id` (string)
*   `user_id` (string)
*   `timestamp` (ISO 8601 string)
*   `amount` (float or string representing a float)
*   `currency` (string)

### 2. Processing & Hash-based Deduplication
You must extract all records from the three files.
Because of upstream retries, the same logical transaction might appear multiple times, sometimes with a different `delivery_id`.
To deduplicate, compute a SHA-256 hash fingerprint for each record using the concatenated string of: `<user_id>|<timestamp>|<amount>` (where amount is formatted to exactly 2 decimal places, e.g., "150.00").
*   Drop any record whose fingerprint has already been seen in the current pipeline run.
*   Retain the *first* occurrence of a record (and its associated `delivery_id`). Process the files in this order: CSV, JSON, XML.

### 3. Pipeline Logging
Your script must append monitoring metrics to `/home/user/etl/pipeline.log`.
The log must contain exactly these lines at the end of the run:
```text
[EXTRACT] records_read=<total_number_of_records_parsed_across_all_files>
[TRANSFORM] duplicates_dropped=<number_of_records_dropped>
[LOAD] records_written=<final_number_of_unique_records>
```

### 4. Output Format
Write the cleaned, deduplicated records to `/home/user/etl/output/clean_transactions.jsonl` (JSON Lines format).
Each line must be a valid JSON object containing all original fields: `delivery_id`, `user_id`, `timestamp`, `amount` (as a float), and `currency`.
The records in the JSONL file must be sorted chronologically by `timestamp` in ascending order.

Ensure your script is executable and can be run with standard Python 3. You may install dependencies via `pip` if necessary, but standard libraries are sufficient.