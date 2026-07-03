You are acting as a log analyst investigating patterns from a faulty ETL pipeline. The pipeline failed and retried multiple times, resulting in duplicate records in the log dump. Your objective is to write a C++ program that parses this log file, extracts structured information from the unstructured payload, deduplicates the logical events, and extracts specific aggregated features.

The log file is located at `/home/user/etl_dump.log`. Each line in the file has the following pipe-separated (`|`) format:
`TIMESTAMP | TXN_ID | USER_ID | RAW_PAYLOAD`

The `RAW_PAYLOAD` contains arbitrary text followed by a structured data block formatted exactly like this: `DATA={key1: "value1", key2: "value2", ...}`.

Your C++ program must perform the following steps:
1. **Deduplication:** The ETL job produced duplicate records upon retrying. A record is considered a duplicate if it has the exact same `USER_ID` and `RAW_PAYLOAD` as a previously processed record. You must ignore `TIMESTAMP` and `TXN_ID` when determining duplicates. Keep only the first occurrence of each unique `(USER_ID, RAW_PAYLOAD)` pair.
2. **Information Extraction:** From the deduplicated records, parse the `DATA={...}` block in the `RAW_PAYLOAD`. You need to extract the values for the keys `"action"`, `"amount"`, and `"ip"`.
3. **Normalization:** 
   - Convert the `"action"` string to lowercase.
   - Parse the `"amount"` string as an integer.
4. **Feature Extraction:** For each unique `USER_ID`, calculate:
   - The total sum of `"amount"` where the normalized `"action"` is exactly `"purchase"`.
   - A sorted, semicolon-separated list of all unique `"ip"` addresses associated with that user across all their deduplicated records (regardless of the action).

Write your code in `/home/user/process_logs.cpp`, compile it (e.g., using `g++ -std=c++17 -O3 process_logs.cpp -o process_logs`), and run it.

Your program must generate an output CSV file at `/home/user/user_features.csv` with the following header:
`user_id,total_purchase_amount,unique_ips`

The rows must be sorted lexicographically by `user_id`.

Example Output (`/home/user/user_features.csv`):
```csv
user_id,total_purchase_amount,unique_ips
U101,250,10.0.0.1;192.168.1.5
U102,0,172.16.0.2
```

Ensure your C++ program handles the entire pipeline efficiently. You may use standard C++ libraries. Do not use external libraries that require installation via package managers.