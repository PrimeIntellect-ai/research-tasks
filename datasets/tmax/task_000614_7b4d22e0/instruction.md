You are a storage administrator tasked with optimizing disk space utilization for a logging cluster. A legacy application continuously generates highly bloated, multi-line diagnostic logs. These logs are spooling rapidly and consuming too much disk space. 

Your objective is to intercept these logs, extract only the essential operational data, convert it into a compact tabular format, and create a highly compressed archive.

Currently, there is a multi-service setup on this server:
1. A Python log generator service running in the background.
2. A local TCP log receiver (listening on port 9001) that writes raw logs to `/home/user/incoming/spool.tar`. (This `.tar` contains multiple nested directories and loose text files with multi-line log records).
3. A local HTTP dashboard service (listening on port 8080) that monitors disk usage.

The raw log records in the extracted text files look like this:
```
=== RECORD START ===
Timestamp: 2023-10-24T10:00:00Z
Severity: CRITICAL
Message: 
  Database connection timeout.
  Retrying in 5 seconds...
  [Traceback data...]
Bloat-Padding: [Thousands of useless characters...]
=== RECORD END ===
```

Your task:
1. Write a Bash script at `/home/user/optimize_logs.sh`.
2. The script must extract `/home/user/incoming/spool.tar`. Handle any nested directories or multi-part archives inside it if necessary.
3. Parse all the extracted text files to find the multi-line records.
4. Extract ONLY the `Timestamp`, `Severity`, and the first line of the `Message` for each record.
5. Convert this parsed data into a single strict CSV file named `summary.csv` with the headers: `Time,Level,Error`.
6. Compress `summary.csv` into a maximally compressed xz archive named `/home/user/processed/final_archive.tar.xz`.
7. The script must be fully automated and executable. 

To prove your script works, execute it so that `/home/user/processed/final_archive.tar.xz` is generated. Our automated system will evaluate your success based on the exact size of the resulting archive (it must be extremely small, proving the bloat was successfully stripped) and the integrity of the compressed CSV data.