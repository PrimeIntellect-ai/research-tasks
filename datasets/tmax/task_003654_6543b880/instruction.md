You are acting as a log analyst investigating access patterns for a web application. You have received a batch of raw access logs, but they contain duplicate entries and sensitive Personally Identifiable Information (PII) that must be handled before the analysis can be shared. 

Your task is to write a Rust program that processes these logs, anonymizes the PII, deduplicates the entries using a hash-based approach, and generates a summary HTML report using a provided template.

**Input Files:**
1. `/home/user/raw_logs.jsonl`: A JSON Lines file where each line is a log entry with the following fields:
   `{"timestamp": "...", "ip": "...", "email": "...", "action": "...", "status": <int>}`
2. `/home/user/report_template.html`: An HTML template containing placeholders for the final report.

**Processing Requirements:**
1. **Deduplication (Hash-based):** 
   You must deduplicate the log entries. Two entries are considered duplicates if the SHA-256 hash of the concatenated string `{action}-{status}-{email}` is identical. You must retain only the *first* occurrence of each unique hash (based on the order in the input file) and discard subsequent duplicates.

2. **Data Masking and Anonymization:**
   For the unique logs retained after deduplication, apply the following masking rules:
   * **IP Address:** Mask the first three octets of the IPv4 address with `XXX`, leaving only the last octet. (e.g., `192.168.1.42` becomes `XXX.XXX.XXX.42`).
   * **Email Address:** Mask the local part (before the `@`) completely with exactly three asterisks `***`, leaving the domain intact. (e.g., `john.doe@example.com` becomes `***@example.com`).

3. **Output Files:**
   * `/home/user/clean_logs.jsonl`: Write the deduplicated, masked log entries here in JSON Lines format, preserving the original fields (`timestamp`, `ip`, `email`, `action`, `status`) but with the updated/masked values.
   * `/home/user/summary.html`: Read `/home/user/report_template.html` and replace the following exact placeholders:
     * `{{TOTAL_RAW}}` -> The total number of lines in `raw_logs.jsonl`.
     * `{{TOTAL_UNIQUE}}` -> The total number of unique log entries after deduplication.
     * `{{TOP_ACTION}}` -> The string value of the `action` field that appears most frequently among the *unique* logs (if there is a tie, pick any).

**Constraints:**
* You must implement the solution in Rust. You may use standard tools like `cargo` to create your project in `/home/user/log_processor` and add dependencies like `serde`, `serde_json`, and `sha2` to your `Cargo.toml`.
* Ensure the final output files are placed exactly at the specified paths.