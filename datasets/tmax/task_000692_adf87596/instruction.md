You are acting as a DevSecOps engineer implementing a "Policy as Code" evaluation engine. 

We recently received a security memo from the CISO detailing our updated intrusion detection and configuration baseline policies. Unfortunately, the memo was only provided as a scanned image, located at `/app/policy_memo.png`.

Your task is to write a Python script that analyzes an environment and enforces the policies outlined in the image. You have been provided with a dataset to evaluate:
1. An authentication log file at `/app/auth.log` containing login attempts.
2. A directory of configuration files at `/app/configs/`. Each configuration file contains key-value pairs, including API tokens that must follow the newly mandated format.

Write a Python script (you can name it whatever you like) that parses these resources, extracts the hidden rules from `/app/policy_memo.png` (using OCR or your vision capabilities), and produces a JSON report of all violations.

Your script must output exactly one file at `/home/user/results.json` with the following structure:
```json
{
  "blocked_ips": ["192.168.1.50", "10.0.0.5"],
  "non_compliant_files": ["/app/configs/db.conf", "/app/configs/cache.yaml"]
}
```

Definitions for the output:
- `blocked_ips`: A list of strings representing IP addresses that violate the failed login threshold policy described in the memo.
- `non_compliant_files`: A list of strings representing absolute paths to files in `/app/configs/` that either:
    a) Violate the strict file permission policy described in the memo.
    b) Contain an invalid API token format (tokens are stored as `api_token=...` inside the files).

The verification suite will compare your `/home/user/results.json` against a hidden ground-truth file. Your score will be the Jaccard similarity index of your detected violations versus the true violations. You must achieve a similarity score of >= 0.95 to pass.

Ensure your code is efficient and handles edge cases such as timestamp parsing and windowed aggregations correctly.