You are a log analyst investigating access patterns across several microservices. You have been given two datasets: a user metadata file and a raw access log file. 

Your task is to write a Go program that processes these files to determine the number of unique access events per user role.

**Input Files:**
1. `/home/user/users.csv`: A CSV file containing user information.
   - Columns: `id,username,role`
   - *Note:* The `username` field may contain leading/trailing spaces and inconsistent capitalization.
2. `/home/user/access_logs.jsonl`: A large JSON-Lines file containing raw access logs.
   - Each line is a JSON object with keys: `timestamp` (ISO8601 format), `username`, `endpoint`, and `ip`.
   - *Note:* This file could be very large; your Go program must stream the file line-by-line rather than loading it entirely into memory.

**Processing Requirements:**
1. **Normalization:** 
   - Normalize all usernames from both files by trimming leading/trailing whitespace and converting them to strictly lowercase.
2. **Join/Merge:** 
   - Map each log entry to a `role` using the normalized username from the CSV. 
   - If a username in the logs does not exist in the `users.csv` file, ignore that log entry completely.
3. **Deduplication:** 
   - We only want to count *unique* requests. A request is considered a duplicate if it has the same normalized `username`, the same `endpoint`, and occurs within the same minute.
   - To do this, truncate the `timestamp` to the minute (e.g., `2023-10-01T14:32:45Z` becomes `2023-10-01T14:32`).
   - Deduplicate based on the composite key of: `normalized_username` + `endpoint` + `truncated_timestamp`.
4. **Aggregation:** 
   - Count the total number of unique, deduplicated requests for each `role`.

**Output:**
Write the final aggregated counts to `/home/user/role_summary.json`.
The output must be a single JSON object where the keys are the role names and the values are the integer counts. 
Example format:
```json
{
  "admin": 45,
  "user": 120,
  "guest": 12
}
```

Write and execute your Go program to produce the final `/home/user/role_summary.json` file.