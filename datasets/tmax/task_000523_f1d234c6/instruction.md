You are a DevSecOps engineer enforcing a "policy as code" standard for an application's traffic logs. A recent capture of HTTP response data has been saved to `/home/user/traffic.json`. This file contains an array of JSON objects, each representing an HTTP response and containing an `ip` field and a `headers` dictionary.

Your task is to write and execute a Python script that sanitizes this log file and extracts actionable network intelligence based on our security policies.

Please perform the following steps:

1. **HTTP Header Inspection & Redaction:**
   Read `/home/user/traffic.json`. Iterate through each record and apply the following redaction rules:
   - **Authentication:** If an `Authorization` header is present, change its value entirely to the string `[REDACTED]`.
   - **Insecure Cookies:** Inspect any `Set-Cookie` headers. If a `Set-Cookie` header is missing either the `Secure` directive or the `HttpOnly` directive (assume case-insensitive substring matching for these directives), replace the entire `Set-Cookie` value with the string `[REDACTED]`. 

2. **Network Policy Action:**
   Keep track of the `ip` addresses associated with any response that served an insecure cookie (i.e., triggered the `Set-Cookie` redaction rule above). 

3. **Output & Access Control:**
   - Save the modified JSON array to `/home/user/clean_traffic.json` with standard formatting (e.g., indent=2).
   - Enforce strict access control: configure the file permissions of `/home/user/clean_traffic.json` to exactly `0600` (read and write for the owner only).
   - Write the list of unique IP addresses that served insecure cookies to `/home/user/blocked_ips.txt`, one IP address per line, sorted in ascending alphabetical order.

Complete these steps using a Python script or terminal commands. Ensure the final output files exist exactly at the specified paths.