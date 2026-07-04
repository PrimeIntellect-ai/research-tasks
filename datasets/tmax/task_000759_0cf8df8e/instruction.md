You are a data engineer tasked with fixing a broken Go-based ETL pipeline. 

There is an existing Go script at `/home/user/etl.go` that reads event data from `/home/user/source.csv` and inserts it into an SQLite database at `/home/user/data.db`. 

Currently, the pipeline has several issues:
1. It crashes when encountering malformed data (invalid timestamps), halting the entire pipeline.
2. It lacks idempotency. If the script is retried after a failure, it attempts to insert duplicate records, which causes primary key constraint violations or duplicates.
3. It is missing the required data sampling and feature extraction logic.

Your task is to fix and complete `/home/user/etl.go` with the following requirements:

1. **Error Handling & Logging**: Catch any rows with an invalid RFC3339 `timestamp`. Do not crash. Instead, skip the row and append the `event_id` of the skipped row to a log file at `/home/user/etl_errors.log` (one `event_id` per line).
2. **Idempotent DB Inserts**: Modify the SQLite insert query so that it is idempotent. If a record with the same `event_id` already exists, it should update/replace the existing record instead of failing or creating duplicates. 
3. **Feature Extraction**: Parse the valid RFC3339 `timestamp` and extract two features to store in the database:
   - `hour`: The hour of the day (integer, 0-23).
   - `is_weekend`: A boolean indicating if the day is Saturday or Sunday (true/false).
4. **Data Sampling**: Only process and insert events where the `user_id` ends with the uppercase letter 'A' or 'B'. Skip all others (these skipped due to sampling should *not* be logged as errors).
5. **Execution & Export**: 
   - Run your fixed Go script to process the data.
   - Once the database is populated, export the entire `events` table to `/home/user/final_export.csv` (must include column headers matching the database schema). You can use the `sqlite3` CLI or write Go code to do this.

**Existing Database Schema (`/home/user/data.db`):**
```sql
CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    user_id TEXT,
    event_type TEXT,
    timestamp TEXT,
    hour INTEGER,
    is_weekend BOOLEAN
);
```

**Source CSV Format (`/home/user/source.csv`):**
Columns: `event_id,user_id,event_type,timestamp`

Ensure your final script runs completely without errors and populates the database and CSV export correctly.