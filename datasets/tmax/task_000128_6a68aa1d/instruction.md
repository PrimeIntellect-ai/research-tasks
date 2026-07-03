You are a log analyst investigating access patterns for a web service. You need to build a data processing pipeline in Python to validate, clean, anonymize, aggregate, and analyze access logs. 

Raw logs are provided in a JSON Lines file at `/home/user/raw_logs.jsonl`.

Write and execute a Python script (e.g., `/home/user/process_logs.py`) that performs the following phases:

**Phase 1: Validation Checkpoint (Quality Gate)**
Read `/home/user/raw_logs.jsonl`. A valid log entry must be a JSON object containing exactly these fields with the correct types:
- `timestamp`: string
- `ip_address`: string (IPv4 format)
- `user_email`: string
- `endpoint`: string
- `status`: integer

If a log entry is missing any of these fields, has extra fields, or has incorrect types, it is invalid. 
Write all invalid log entries exactly as they appeared (raw JSON strings) to `/home/user/output/invalid.jsonl`.

**Phase 2: Data Masking and Anonymization**
For all *valid* log entries, apply the following masking rules:
1. `user_email`: Replace the original email with its SHA-256 hash (lowercase hex string).
2. `ip_address`: Mask the last octet of the IPv4 address with `0` (e.g., `192.168.1.105` becomes `192.168.1.0`).

Save these cleaned and masked valid logs to `/home/user/output/masked_logs.jsonl`.

**Phase 3: Summary Statistics**
Using the masked valid logs, calculate the total number of requests originating from each masked `ip_address`.
Write the results to a CSV file at `/home/user/output/summary.csv` with the headers `ip_address,request_count`. 
Sort the CSV by `request_count` in descending order. If there is a tie, sort alphabetically by `ip_address`.

**Phase 4: Similarity Computation (Anomaly Detection)**
We want to find users who exhibit highly similar browsing patterns. 
Using the valid masked logs:
1. For each masked `user_email`, compile a mathematical *set* of all unique `endpoint`s they accessed. (Ignore users who accessed 0 valid endpoints).
2. Compute the Jaccard similarity between the endpoint sets of every unique pair of users. (Jaccard similarity = size of intersection / size of union).
3. Find the pair of users with the highest Jaccard similarity score. If there is a tie, pick the pair whose combined hashes sort first alphabetically (i.e., compare tuple `(min(user1, user2), max(user1, user2))`).
4. Output the result to `/home/user/output/anomalies.json` in the following format (round similarity to 4 decimal places):
```json
{
  "user1": "<masked_email_hash_1>",
  "user2": "<masked_email_hash_2>",
  "similarity": 0.8571
}
```
*Note: Ensure `user1` is alphabetically before `user2` in the JSON output.*

**Environment setup:**
The output directory `/home/user/output/` does not exist yet. Your script should create it. Do not use external libraries like `pandas` or `scikit-learn`; use standard library Python (e.g., `json`, `csv`, `hashlib`, `itertools`).