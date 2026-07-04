You are an automation specialist managing an ETL pipeline. An upstream job frequently fails and retries, causing exact duplicate records to be appended to our raw event log `/home/user/raw_events.csv`. 

We need a robust C program to process this file, acting as an ETL deduplicator, anonymizer, and aggregator.

Your tasks:
1. Write a C program (save as `/home/user/etl_processor.c`) that reads `/home/user/raw_events.csv`. The CSV has no header. The format is: `timestamp,user_id,name,email,event_type`.
2. The C program must:
   - **Deduplicate**: Ignore any exactly identical rows (same timestamp, user_id, name, email, and event_type).
   - **Mask & Anonymize**: Replace the `name` field with the literal string `MASKED` and the `email` field with `<user_id>@anonymized.local` (e.g., if user_id is 105, the email becomes `105@anonymized.local`).
   - **Output Clean Data**: Write the deduplicated, masked records to `/home/user/clean_events.csv` in the format: `timestamp,user_id,MASKED,<anonymized_email>,event_type`. Keep the original row chronological order for the first appearance of each duplicate.
   - **Bucket & Aggregate**: Group the deduplicated events into 1-hour time buckets based on the Unix timestamp. A bucket starts exactly at the hour mark (e.g., timestamp `1700003700` belongs to bucket `1700002800` because `1700003700 / 3600 * 3600 = 1700002800`). Count the number of events per `event_type` in each bucket.
   - **Output Aggregations**: Write the aggregated counts to `/home/user/aggregated_events.csv` in the format: `bucket_start_timestamp,event_type,count`. Sort the output ascending by `bucket_start_timestamp`, then alphabetically by `event_type`.
3. Create a bash script `/home/user/run_pipeline.sh` that compiles `/home/user/etl_processor.c` (into `etl_processor`) and then executes it. Ensure the script is executable.
4. Write a cron schedule definition to `/home/user/cron.txt` that schedules `/home/user/run_pipeline.sh` to run exactly at the top of every hour (minute 0).

Ensure all code compiles without errors and writes outputs strictly in the specified formats.