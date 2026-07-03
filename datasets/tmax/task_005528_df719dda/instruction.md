You are a log analyst investigating a recent spike in suspicious activity. You have two files to analyze:
1. `/home/user/access.log`: A JSON Lines file containing recent server access logs. Each line is a JSON object with at least `ts` (ISO8601 timestamp string) and `ip` (string) fields.
2. `/home/user/threat_ips.csv`: A CSV file containing known malicious IP addresses. The file has no header, and the first column is the IP address.

Your task is to write a Go program `/home/user/analyze.go` that performs the following data processing pipeline:
1. **Join/Filter**: Read both files and filter the access logs so you only process events from IPs that exist in the `threat_ips.csv` file.
2. **Feature Extraction & Time-Based Bucketing**: Extract the timestamp (`ts`) and round it *down* to the nearest 5-minute boundary (e.g., `2023-10-01T10:04:55Z` becomes `2023-10-01T10:00:00Z`, and `2023-10-01T10:06:05Z` becomes `2023-10-01T10:05:00Z`). Format the bucketed time as an ISO8601 string in UTC (e.g., `2006-01-02T15:04:05Z`).
3. **Windowed Aggregation**: Count the number of requests per malicious IP within each 5-minute bucket.
4. **Database Bulk Export**: Create a SQLite database at `/home/user/threat_activity.db`. Create a table named `activity_summary` with the following schema:
   - `bucket_time` (TEXT)
   - `ip` (TEXT)
   - `request_count` (INTEGER)
   Insert all the aggregated records into this table.

Requirements:
- Ensure your Go code creates the SQLite database file if it does not exist.
- Use `github.com/mattn/go-sqlite3` for SQLite operations in Go. You will need to initialize a Go module and fetch this dependency.
- Once your Go program is written, execute it so that `/home/user/threat_activity.db` is successfully generated and populated.