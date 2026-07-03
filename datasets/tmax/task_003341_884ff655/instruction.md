You are acting as a data analyst for our e-commerce platform. We are trying to reconcile user reviews with our server ingest logs to flag potentially spoofed submissions. 

You have been provided with two input datasets:
1. A CSV file containing customer reviews at `/home/user/data/reviews.csv`. 
2. A JSON Lines file containing server ingest logs at `/home/user/data/server_logs.jsonl`.

Unfortunately, the `reviews.csv` file is notoriously difficult to parse because the `review_text` column contains unescaped embedded newlines, which causes naive data pipelines to drop rows or misalign columns. 

Your objective is to write and execute a Python script that performs the following ETL pipeline:
1. **Dependency Installation**: Install any necessary Python packages to your environment (e.g., `pandas`, `pyarrow`).
2. **Robust Extraction**: Read `reviews.csv` and `server_logs.jsonl`. Ensure no rows are dropped from the CSV due to embedded newlines.
3. **Timestamp Alignment**: 
   - The CSV file has a `submitted_at` column in the format `YYYY-MM-DD HH:MM:SS` (assumed UTC).
   - The JSONL file has an `ingest_epoch` column representing the Unix timestamp (seconds).
   - Convert both to a unified datetime format (UTC).
4. **Data Merge**: Join the two datasets on the `review_id` column.
5. **Validation & Transformation**: Create a new boolean column named `is_verified`. This should be `True` if the absolute difference between `submitted_at` and `ingest_epoch` is strictly less than 10 seconds, and `False` otherwise.
6. **Load**: Write the resulting joined dataframe to a Parquet file at `/home/user/output/verified_reviews.parquet`.

The final Parquet file must contain the following columns:
- `review_id` (string)
- `user_id` (string)
- `submitted_at` (timestamp)
- `review_text` (string)
- `ingest_epoch` (timestamp)
- `server_ip` (string)
- `is_verified` (boolean)

Ensure your script handles the embedded newlines correctly so that the total row count in the output exactly matches the total valid distinct reviews in the input datasets. Execute your script to generate the final Parquet file.