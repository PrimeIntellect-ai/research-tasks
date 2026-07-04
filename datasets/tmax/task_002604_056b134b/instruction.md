You are an automation specialist managing a server infrastructure inventory. The upstream system frequently exports messy data, and you need to build a robust ETL pipeline to process it.

You have a raw CSV file at `/home/user/inventory.csv` containing server details. The file has a header and uses commas as delimiters. Some text fields in the CSV improperly contain embedded newline characters which break standard line-by-line parsers.

The columns are: `ServerID,Hostname,OS,Notes,Status`

Write a Bash script at `/home/user/process_inventory.sh` (make sure it is executable) that performs the following pipeline operations:

1. **Cleaning (Drop Embedded Newlines):** Parse the CSV properly and silently *drop* any rows where the `Notes` field contains an embedded newline character (`\n`). 
2. **Deduplication:** Deduplicate the remaining rows based on `ServerID`. If there are multiple rows with the same `ServerID`, keep *only the last* occurrence in the file.
3. **Normalization:** 
   - Convert all `Hostname` values to strict lowercase.
   - Convert all `OS` values to strict uppercase.
4. **Template Generation:** Filter the cleaned, deduplicated, and normalized records to find only those where `Status` is exactly `active`. For each of these active servers, append a text block to `/home/user/active_servers.conf` using exactly this template:
```
[<Hostname_in_lowercase>]
ServerID=<ServerID>
OperatingSystem=<OS_IN_UPPERCASE>
Info=<Notes>
---
```
5. **Logging:** While processing, your script must write a log file to `/home/user/process.log` containing exactly these lines in order (replace the bracketed placeholders with the actual integer counts):
```
[INFO] Pipeline started
[INFO] Dropped rows with embedded newlines: <count_dropped>
[INFO] Total unique servers after deduplication: <count_unique>
[INFO] Active servers written to config: <count_active>
[INFO] Pipeline finished
```

**Notes:**
- You may use any standard tools available in a Linux environment (e.g., Python, awk, jq, etc.) within your Bash script to handle the CSV parsing safely.
- Ignore the header row when calculating metrics and do not write the header to the config file.