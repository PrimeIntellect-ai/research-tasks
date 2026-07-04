You are an automation specialist responsible for fixing and improving an ETL pipeline. 

We have a system that extracts global user feedback logs into daily JSONL files. Recently, upstream retries have been creating overlapping extracts, leading to duplicate records. Your task is to write a robust, idempotent Python ETL script that processes these files, deduplicates the data, aggregates it into time-series buckets, and generates a formatted text report.

Create a Python script at `/home/user/etl.py` that meets the following requirements:

1. **Input & Parallel Processing:**
   - The script must take exactly two command-line arguments: an input directory and an output directory. 
   - Example: `python3 /home/user/etl.py /home/user/input /home/user/output`
   - Read all `.jsonl` files in the input directory. You must use Python's `multiprocessing` or `concurrent.futures` module to process the files in parallel (e.g., reading and parsing each file in a separate process/thread).

2. **Deduplication:**
   - Each JSON line has the format: `{"ts": "<ISO8601-timestamp>", "id": "<unique-string>", "text": "<unicode-message>", "lang": "<language-code>"}`.
   - Globally deduplicate all records based on the `id` field. If multiple records have the same `id`, keep only one of them (it does not matter which).

3. **Time-based Bucketing & Aggregation:**
   - Truncate the `ts` timestamp to the start of the hour (e.g., `2023-10-01T14:32:00Z` becomes `2023-10-01T14:00:00Z`).
   - Group the deduplicated records by this hourly bucket.
   - For each hourly bucket, calculate the number of *unique* languages (`lang`).
   - Find the "Sample" text for each hour, which is defined as the lexicographically first `text` string among the records in that hour (based on standard Python string sorting).

4. **Template-based Generation:**
   - For each hour, generate a summary string formatted exactly as:
     `Hour: {hour} | Unique Langs: {lang_count} | Sample: {sample_text}`
   - Ensure the script creates the output directory if it doesn't exist, and write the generated strings to `/home/user/output/summary.txt`.
   - The lines in `summary.txt` must be sorted chronologically by the hour bucket.
   - The script must be idempotent. Rerunning it on the same input and output directories must completely overwrite `summary.txt` and produce the exact same result without duplicate lines.

5. **Logging:**
   - Implement pipeline logging using Python's built-in `logging` module.
   - Log to the file `/home/user/pipeline.log`.
   - The log must include an `INFO` level message containing the total number of unique records processed, in the format: `Total unique records: <N>`.

Write the script and test it on the existing data in `/home/user/input`.