You are acting as a log analyst for a tech company. We recently discovered that a misconfigured application has been logging sensitive Personally Identifiable Information (PII) in our raw server access logs. 

Your task is to write and execute a Python script that reads a messy raw log file, extracts the relevant fields using regular expressions, normalizes the data, masks the sensitive PII, and outputs the cleaned data to a structured JSON Lines file.

**Input:**
You have a log file located at: `/home/user/raw_server.log`

The log lines are somewhat inconsistent but generally contain:
- A timestamp (in either `[DD/MMM/YYYY:HH:MM:SS +0000]` or `[YYYY-MM-DDTHH:MM:SSZ]` format)
- An HTTP request line in quotes (e.g., `"GET /api/v1/users?id=5 HTTP/1.1"`)
- An HTTP status code (e.g., `200`)
- Bytes sent (e.g., `1024`)
- An IP address prefixed by `IP: ` (e.g., `IP: 192.168.1.50`)
- Optional sensitive data floating in the log line, which could include Emails, Credit Card numbers (16 digits separated by hyphens), or Social Security Numbers (9 digits separated by hyphens: XXX-XX-XXXX).

**Processing Requirements:**

1. **Extraction:** Parse each line to extract the timestamp, HTTP method, URL path (excluding query parameters), status code, bytes, and IP address. Also, detect any Emails, Credit Cards, or SSNs anywhere in the line.
2. **Normalization:**
   - Standardize all timestamps to exact ISO 8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ` (Assume month abbreviations are standard English, e.g., Oct).
   - Convert all URL paths to strict lowercase (e.g., `/API/V1/PAYMENTS` becomes `/api/v1/payments`).
   - Cast status code and bytes to integers.
3. **Anonymization & Masking:**
   - **IP Addresses:** Mask the last octet with `XXX` (e.g., `192.168.1.50` becomes `192.168.1.XXX`).
   - **Emails:** Keep the first character of the local part, mask the rest of the local part with exactly five asterisks `*****`, and keep the domain intact (e.g., `john.doe@email.com` becomes `j*****@email.com`).
   - **Credit Cards:** Mask the first 12 digits with `X` but keep the hyphens and the last 4 digits (e.g., `1234-5678-9012-3456` becomes `XXXX-XXXX-XXXX-3456`).
   - **SSNs:** Mask the first 5 digits with `X`, keeping the hyphens (e.g., `111-22-3333` becomes `XXX-XX-3333`).

**Output:**
Write the processed and cleaned logs to `/home/user/processed_logs.jsonl`.
Each line in this file must be a valid JSON object representing a single log event with the following keys:
- `"timestamp"` (string, normalized)
- `"method"` (string, e.g., "GET")
- `"path"` (string, normalized, no query params)
- `"status"` (integer)
- `"bytes"` (integer)
- `"ip"` (string, masked)
- `"pii_detected"` (dictionary) containing keys `"emails"`, `"credit_cards"`, and `"ssns"`. Each key should map to a list of the *masked* values found in that line. If none are found for a category, it should be an empty list `[]`.

Write your Python script, execute it, and ensure the output file is generated correctly.