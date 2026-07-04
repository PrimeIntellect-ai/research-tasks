You are a data engineer responsible for processing server logs into structured analytics using Python. 

A raw log file is located at `/home/user/raw_logs.txt`. The log lines contain a mix of structured headers and unstructured text messages. 
Example line:
`2023-10-01T14:32:01Z | ERROR | Process failed. Client IP: 192.168.1.50, Time taken: 120ms, ErrorCode: E404`

Your goal is to write a Python script that acts as an ETL pipeline to process these logs. The pipeline must implement the following steps:

1. **Extraction**: Parse each line to extract the Timestamp, Level, IP address, Duration (as an integer), and ErrorCode. Ignore lines that do not have `Client IP:`, `Time taken:`, and `ErrorCode:`.
2. **Validation Checkpoint**: Filter out invalid records. A record is invalid if the Duration is negative (< 0) OR if the IP address does not strictly match a standard IPv4 format (`X.X.X.X` where X is 1-3 digits). Write the original, raw text of all invalid lines to `/home/user/rejected_logs.txt`.
3. **Hash-Based Deduplication**: Our system sometimes retries failed requests, generating duplicate logs. We consider an event a duplicate if it has the exact same IP address, ErrorCode, and Duration. Compute a SHA-256 hash of the string `<IP>_<ErrorCode>_<Duration>` for each valid record. Only keep the *first* occurrence of each hash.
4. **Aggregation**: For the deduplicated valid records, calculate summary statistics per ErrorCode. We need the total count of unique events and the average duration (rounded to exactly 2 decimal places).
5. **Output generation**:
   - Write the valid, deduplicated records to `/home/user/clean_events.jsonl` as JSON Lines. Each line must be a JSON object with keys: `timestamp`, `level`, `ip`, `duration` (as integer), and `code`.
   - Write the aggregated statistics to `/home/user/stats.csv`. The file must have the header `ErrorCode,EventCount,AvgDuration`. Order the rows alphabetically by `ErrorCode`.

Please write and execute the Python script to produce the three output files (`rejected_logs.txt`, `clean_events.jsonl`, `stats.csv`).