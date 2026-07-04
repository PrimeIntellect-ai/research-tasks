You are tasked with building a resilient configuration processing pipeline using Bash. 

We have a legacy configuration parser located at `/app/config_processor`. This stripped binary reads CSV data from standard input (expected columns: `timestamp,config_key,config_value`) and outputs a parsed text format. Unfortunately, it has known bugs: it silently drops rows containing embedded newlines within quoted fields, and it completely corrupts data if the character encoding is not strictly UTF-8 (e.g., it fails on UTF-16LE or ISO-8859-1 inputs).

Your objective is to create a multi-stage Bash-based HTTP service that wraps this binary, fixes the input data, and post-processes the output. 

Requirements:
1. Bring up an HTTP service listening on `127.0.0.1:9090`. You may use `socat`, `nc`, or write a basic Bash HTTP wrapper.
2. The service must accept `POST /process` requests containing raw CSV data in the body.
3. **Encoding Handling:** Detect if the incoming payload is UTF-16LE or ISO-8859-1 and convert it to UTF-8. 
4. **Newline Cleaning:** Parse the CSV and replace any embedded newlines within quoted CSV fields with a single space character, ensuring the `/app/config_processor` does not drop these rows.
5. Pass the cleaned CSV to `/app/config_processor`.
6. **Resampling and Gap-Filling:** The binary will output lines in the format `timestamp,config_key,config_value` (where timestamp is a Unix epoch integer). The output timestamps may have gaps. Post-process this output in Bash to resample the data into strictly 60-second intervals. If a 60-second interval is missing for a given `config_key`, carry forward the last known `config_value` for that key.
7. Return the final, gap-filled CSV as the HTTP response body with a `200 OK` status.
8. **Scheduling:** Create a cron job for the `user` that runs every 5 minutes, executing `/app/health_check.sh` (you must create a dummy script at this location that echoes "OK" to `/tmp/health.log`).

Ensure your service runs continuously in the background and correctly handles sequential requests.