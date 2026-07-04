We had an ETL job that failed and retried multiple times over the weekend. As a result, our raw event log is massive and contains millions of duplicate records. I need you to build a Python pipeline to clean this data, extract a representative sample, and load the results into a database for our analytics team. 

The raw data is located at `/home/user/data/raw_events.csv`. It has the following columns:
`event_id, user_id, event_type, timestamp, payload`

Please write a Python script at `/home/user/process_pipeline.py` that performs the following steps:

1. **Large-file streaming & Hash-based deduplication**: 
   Read `/home/user/data/raw_events.csv` in a streaming fashion (do not load the entire file into memory at once). 
   Deduplicate the records based on the MD5 hash of the concatenated string of `user_id`, `event_type`, and `payload` (i.e., `md5(f"{user_id}{event_type}{payload}".encode('utf-8')).hexdigest()`). 
   If multiple records yield the same hash, keep *only the first one* you encounter in the file.
   Write the deduplicated records to `/home/user/data/clean_events.csv` (include the header).

2. **Stratified Sampling**:
   From your deduplicated dataset, create a stratified sample representing exactly 10% of the data per `event_type`.
   To ensure reproducible results without relying on random seeds: group the clean data by `event_type`, sort each group by `event_id` in ascending alphabetical order, and select every 10th record (0-indexed, so pick index 0, 10, 20, etc., within each group).
   Write this sample to `/home/user/data/sampled_events.csv` (include the header).

3. **Database Bulk Import**:
   Create an SQLite database at `/home/user/data/analytics.db`.
   Bulk load the `clean_events.csv` into a table named `clean_events`.
   Bulk load the `sampled_events.csv` into a table named `sampled_events`.
   Ensure both tables have the schema: `(event_id TEXT, user_id TEXT, event_type TEXT, timestamp TEXT, payload TEXT)`.

You must execute your script to produce the final CSVs and the SQLite database. I will verify the integrity of the SQLite database tables and their row counts.