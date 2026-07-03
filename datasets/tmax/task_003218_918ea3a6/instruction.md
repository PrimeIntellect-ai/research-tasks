You are a data analyst tasked with processing a batch of legacy server performance logs. The data has been collected from different systems and dropped into `/home/user/raw_data/`. Due to the diverse origins of the data, the CSV files have different character encodings.

Your objective is to create a robust data processing pipeline using only standard Bash tools (like `awk`, `sed`, `iconv`, `sort`, `sqlite3`, etc.) to clean, merge, analyze, and load this data.

Perform the following steps:

1. **Encoding Normalization**: Identify the character encoding of each `.csv` file in `/home/user/raw_data/` and convert the content of all files to standard `UTF-8`.
2. **Merge and Sort**: Combine all the records into a single file at `/home/user/combined.csv`. The combined file must:
   - Contain exactly one header row (`id,timestamp,server_name,response_time_ms`).
   - Have all data rows sorted chronologically by the `timestamp` column (oldest to newest).
3. **Changepoint Anomaly Detection**: Analyze `/home/user/combined.csv` to detect sudden spikes in response time. We define a "changepoint anomaly" as any data row where the `response_time_ms` is **strictly greater than 3 times** the `response_time_ms` of the *immediately preceding chronological row* in the combined file. 
   - Extract the anomalous rows (including the header) and save them to `/home/user/anomalies.csv`.
4. **Database Bulk Load**: Bulk import the completely cleaned and sorted data from `/home/user/combined.csv` into an SQLite database located at `/home/user/analytics.db`. 
   - The data should be imported into a table named `performance_logs`.

Ensure all output files (`combined.csv`, `anomalies.csv`, `analytics.db`) are correctly placed in `/home/user/`.