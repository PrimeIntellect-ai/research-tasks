As a developer organizing an old project's files, you have discovered some legacy Web Application Firewall (WAF) access logs located in `/home/user/waf_logs/`. These logs are split by region into `us_east.log` and `eu_west.log`.

You need to analyze these logs to identify security threats, merge the findings, and generate a consolidated report in a specific custom format.

Each line in the log files follows this format:
`[TIMESTAMP] HTTP_METHOD /path/to/endpoint?param1=value1&data=ENCODED_PAYLOAD`

Your tasks are:
1. Parse both log files and extract the URL path and query parameters for each entry.
2. Find the `data` query parameter. Its value is always Base64 encoded. Decode this value.
3. Filter the entries: you only care about requests where the decoded `data` payload contains the exact substring `malicious_intent`.
4. Merge the findings from both files. If the exact same decoded malicious payload is observed multiple times (even across different paths or files), group them together.
5. Sort the grouped payloads chronologically by the *earliest* timestamp they were observed.
6. Generate a final report at `/home/user/security_report.txt` using the exact custom format below.

For the report, the paths associated with a given payload must be deduplicated and sorted alphabetically in a comma-separated list.

**Format for `/home/user/security_report.txt`**:
```
REPORT START
[EARLIEST_TIMESTAMP] DECODED_PAYLOAD
Paths: /path1, /path2
---
[EARLIEST_TIMESTAMP] DECODED_PAYLOAD
Paths: /path3
REPORT END
```

*Note: Use standard sorting (lexicographical) for the paths. Make sure exactly one `---` separates each entry block, and the file begins with `REPORT START` and ends with `REPORT END`.*