You are a log analyst investigating patterns in an ETL job that has been producing duplicate records on retry. 

Your task is to write a C program that streams a large log file, filters out malformed records, computes rolling statistics, and extracts aggregated information about the retries.

The log file is located at `/home/user/data/etl_job.log`. 
It is a comma-separated file with the following columns:
`TIMESTAMP,SESSION_ID,RETRY_COUNT,LATENCY,MESSAGE`
- `TIMESTAMP`: integer
- `SESSION_ID`: integer
- `RETRY_COUNT`: integer
- `LATENCY`: float
- `MESSAGE`: string (may contain spaces, extends to the end of the line)

Write a C program at `/home/user/process.c` that does the following:
1. Reads `/home/user/data/etl_job.log` line by line (do not load the entire file into memory, as it is considered a large file stream).
2. Skips any line where the `MESSAGE` field contains non-ASCII characters (any byte with a value > 127).
3. For each `SESSION_ID` in the valid lines, keep track of:
   - The total number of retry events (an event is considered a retry if `RETRY_COUNT > 0`).
   - The rolling average `LATENCY` of the **last 3** valid events for that session. (If a session has fewer than 3 valid events, compute the average of the available valid events).
4. After processing the entire file, output a summary report to `/home/user/report.csv`.
5. The output format for `/home/user/report.csv` must be:
   `SESSION_ID,TOTAL_RETRIES,LAST_3_AVG_LATENCY`
   - `SESSION_ID` should be printed as an integer.
   - `TOTAL_RETRIES` should be the total number of valid events where `RETRY_COUNT > 0` for that session.
   - `LAST_3_AVG_LATENCY` must be printed as a float with exactly 2 decimal places (e.g., `20.00`).
   - Sort the output in ascending order by `SESSION_ID`.

Compile your program using `gcc` and run it to produce `/home/user/report.csv`. Do not leave behind any debug output in the CSV file.