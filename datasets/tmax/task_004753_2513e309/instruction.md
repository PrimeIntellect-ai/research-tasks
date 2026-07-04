You are a data engineer responsible for fixing and deploying a legacy ETL pipeline. The current pipeline frequently produces duplicate records on retry and fails to properly anonymize Personally Identifiable Information (PII) before passing data to a downstream proprietary ingestion engine. 

Your objective is to write a robust Python ETL script and schedule it. 

Here are the requirements:

1. **Analyze the Downstream Binary:**
   The downstream system is a compiled, stripped legacy Linux binary located at `/app/record_ingester`. You do not need to execute it, but you must analyze it. The binary expects all masked SSNs in the incoming data to be replaced with a very specific proprietary placeholder string hardcoded inside the binary. Find this placeholder string (it looks like `[MASKED_...]`).

2. **Develop the ETL Script:**
   Create a Python script at `/home/user/etl_pipeline.py`. 
   - It must accept exactly two command-line arguments: an input directory and an output directory (e.g., `python3 /home/user/etl_pipeline.py <input_dir> <output_dir>`).
   - **Parallel Processing:** It must read and process all `.json` files from the input directory in parallel using Python's `multiprocessing` or `concurrent.futures`.
   - **Data Masking:** Every JSON file contains a list of record objects. For each record, check the `notes` and `user_data` string fields. If you find any Social Security Numbers (format: `XXX-XX-XXXX`), you must replace the SSN with the exact placeholder string you discovered in step 1.
   - **Deduplication:** The pipeline currently creates duplicates if a batch is retried. Across all files in the current input batch, deduplicate records based on the `record_id` field. If multiple records share the same `record_id`, keep only the record with the highest integer `timestamp` value. 
   - Write the cleaned, deduplicated, and masked records to the output directory as a single file named `processed_batch.json` containing a JSON array of the final records.
   - **Logging:** The script must append a log line to `/home/user/etl.log` formatted exactly as: `[YYYY-MM-DD HH:MM:SS] Processed <N> valid records.` where `<N>` is the final count of records written.

3. **Schedule the Pipeline:**
   Configure the system's cron to run your script exactly every 5 minutes. The cron job should run as the `user` user, taking `/home/user/incoming` as the input directory and `/home/user/processed` as the output directory.

Ensure your code is highly robust. An automated verification suite will test your script against a hidden adversarial corpus of data to ensure perfect masking and deduplication.