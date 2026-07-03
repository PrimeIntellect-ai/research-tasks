You are a log analyst investigating a suspected credential stuffing attack on our authentication systems. We have extracted a raw access log file from our web servers, but the logging pipeline experienced an issue, resulting in duplicated entries and unstructured time sequences.

Your task is to process this raw log file using Python and identify specific suspicious IP addresses based on the criteria below. 

**Input File:**
`/home/user/raw_access_logs.jsonl`
Format: JSON Lines (one JSON object per line).
Fields:
- `timestamp`: ISO8601 format (e.g., "2023-10-01T10:03:15Z")
- `ip_address`: IPv4 address string
- `endpoint`: URL path requested
- `status_code`: HTTP status code (integer)
- `request_id`: UUID string
- `payload_hash`: SHA256 hash string of the request payload

**Processing Requirements:**
1. **Deduplication:** The log pipeline accidentally duplicated some events. Filter out duplicates based on the `request_id`. If multiple logs have the same `request_id`, keep only the *first* one you process.
2. **Filtering:** We are only interested in failed login attempts. Filter the logs to keep only records where `endpoint` is `"/login"` and `status_code` is `401`.
3. **Time-Based Bucketing:** Group the filtered logs into 5-minute tumbling windows based on the `timestamp`. For example, times from `10:00:00` to `10:04:59` fall into the `10:00:00` bucket. Format the bucket timestamp as an ISO8601 string (e.g., `2023-10-01T10:00:00Z`).
4. **Aggregation & Grouping:** Within each 5-minute bucket, group the logs by `ip_address`.
5. **Payload Deduplication & Threshold:** For each `(bucket, ip_address)` group, count the number of *unique* `payload_hash` values. We want to find attackers trying many different passwords. If an IP address has strictly **more than 5** unique `payload_hash` values within a single 5-minute bucket, flag it as suspicious.
6. **Sorting:** Sort the final flagged results first by `time_bucket` (ascending), then by `ip_address` (ascending alphabetically).

**Output Requirements:**
Write a Python script to perform this processing. Save your final output to `/home/user/suspicious_activity.json`.
The output must be a well-formatted JSON array of objects, with each object containing exactly these keys:
`time_bucket` (string)
`ip_address` (string)
`unique_payloads` (integer)

Example output format:
```json
[
  {
    "time_bucket": "2023-10-01T10:00:00Z",
    "ip_address": "10.0.0.5",
    "unique_payloads": 6
  }
]
```