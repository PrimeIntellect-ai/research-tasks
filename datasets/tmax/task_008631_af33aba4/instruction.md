You are an automation specialist responsible for creating reliable data workflows. We have a nightly ETL job that pulls transaction records into CSV files, but due to upstream retry mechanisms, the job frequently produces duplicate records across different batch files.

Your task is to write a Go program (`/home/user/etl_pipeline.go`) that acts as a robust ETL orchestrator. It must process all raw CSV files, deduplicate the records, and detect changepoint anomalies in daily transaction volumes.

**Input Data:**
The raw data is located in `/home/user/raw_data/`. There will be multiple CSV files (e.g., `batch1.csv`, `batch2.csv`, `batch2_retry.csv`).
Each CSV file has the following header and columns:
`tx_id,timestamp,user_id,amount`
- `tx_id`: String, unique identifier for a transaction.
- `timestamp`: RFC3339 formatted date-time (e.g., `2023-10-01T10:00:00Z`).
- `user_id`: String.
- `amount`: Float64, the transaction value.

**Processing Requirements:**
1. **Deduplication:** Read all CSV files in the `raw_data` directory. If multiple records have the same `tx_id`, keep *only* the record with the most recent (latest) `timestamp`.
2. **Aggregation & Anomaly Detection:** 
   - Group the deduplicated transactions by date (using the `YYYY-MM-DD` portion of the timestamp).
   - Calculate the average `amount` for each day.
   - Sort the days chronologically.
   - Detect "changepoint" anomalies: If the average transaction amount for a given day deviates by **more than 50%** from the *strictly previous day's* average amount, flag it. 
     - Formula: `|current_day_avg - previous_day_avg| / previous_day_avg > 0.50`
     - The first day in the dataset cannot be an anomaly since there is no previous day.

**Output Requirements:**
The program must create a directory `/home/user/processed/` and generate two files inside it:

1. `/home/user/processed/clean_data.json`: 
   A JSON array containing all deduplicated records, sorted by `tx_id` in ascending alphabetical order. 
   Fields: `{"tx_id": "...", "timestamp": "...", "user_id": "...", "amount": 0.0}`

2. `/home/user/processed/anomalies.json`:
   A JSON array containing the detected anomalies, sorted chronologically. 
   Fields: `{"date": "YYYY-MM-DD", "previous_avg": 0.0, "current_avg": 0.0, "deviation_pct": 0.0}` 
   *(Note: `deviation_pct` should be a percentage expressed as a float, e.g., 50.5 for 50.5%)*.

**Instructions:**
1. Write the Go code in `/home/user/etl_pipeline.go`.
2. Initialize any necessary go modules in `/home/user`.
3. Run the Go program to process the data and generate the output files.