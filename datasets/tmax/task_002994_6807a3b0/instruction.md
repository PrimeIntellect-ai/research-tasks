You are acting as a security log analyst. We have experienced a wave of unauthorized access attempts, and we need to compile a list of unique, anonymized suspect IPs that encountered a `403` (Forbidden) error across our disparate logging systems.

You need to process logs from three different systems, which output in three different formats, located in `/home/user/logs/`:
1. `/home/user/logs/web.csv` - Contains columns: `timestamp`, `status_code`, `ip_address`, `user_agent`.
2. `/home/user/logs/api.json` - Contains a JSON array of objects with keys: `time`, `event`, `client_ip`.
3. `/home/user/logs/legacy.log` - Contains plain text lines.

Your task is to write and run a Python script that does the following:
1. Identifies all log entries across all three files that represent a 403 error. 
   - In `web.csv`, the `status_code` is exactly `403`.
   - In `api.json`, the `event` string contains `403`.
   - In `legacy.log`, the text contains `403`.
2. Extracts the IPv4 addresses associated with these 403 errors. For `legacy.log`, you will need to construct and use a Regex pattern to extract the IPv4 address from the unstructured text.
3. Performs hash-based anonymization and deduplication. Compute the SHA-256 hash (in lowercase hex) of each extracted IPv4 address.
4. Saves the deduplicated, sorted list of SHA-256 hashes to a JSON file at `/home/user/anonymized_ips.json`.

The output file `/home/user/anonymized_ips.json` must contain exactly a single JSON array of strings, sorted alphabetically. Example format:
```json
[
  "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
  "fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9"
]
```
Do not include any IPs that did not encounter a 403 error.