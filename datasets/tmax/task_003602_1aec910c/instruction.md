You are an automation specialist tasked with building a highly efficient data sanitization and aggregation pipeline for a set of raw web server logs. 

We have a directory containing multiple log files at `/home/user/logs/raw/`. These logs contain sensitive Personally Identifiable Information (PII) that must be masked before the data can be used for analytics. Since the dataset can grow large, the sanitization step must be processed in parallel.

Write a Bash script at `/home/user/run_pipeline.sh` that performs the following multi-stage pipeline:

**Phase 1: Parallel Data Masking**
Process all `.log` files in `/home/user/logs/raw/` concurrently (using tools like `xargs -P` or GNU `parallel`) and save the masked versions to `/home/user/logs/clean/` keeping the exact same filenames.
Apply the following regex-based transformations to each line:
1. **IPv4 Addresses:** Replace the last octet of any IP address with `XXX`. (Example: `192.168.1.50` becomes `192.168.1.XXX`)
2. **Email Addresses:** Replace the local-part (before the `@`) of any email address with `***`. (Example: `john.doe@example.com` becomes `***@example.com`)
3. **Credit Card Numbers:** Find any 16-digit credit card formatted exactly as `XXXX-XXXX-XXXX-XXXX` and mask the first 12 digits, leaving the hyphens and the last 4 digits. (Example: `1234-5678-9012-3456` becomes `****-****-****-3456`)

**Phase 2: Feature Extraction and Aggregation**
After all files are successfully sanitized, the script must parse the sanitized logs in `/home/user/logs/clean/` to extract the HTTP status codes and count their frequencies across ALL logs. 
* Assume the log format is always: `[TIMESTAMP] IP_ADDRESS HTTP_METHOD URL STATUS_CODE PAYLOAD` (space-separated up to the payload).
* Output the aggregated counts to a CSV file at `/home/user/logs/summary.csv`.
* The CSV must have a header `status_code,count` and be sorted in descending order of the count. If counts are tied, sort by status_code ascending.

**Requirements:**
- Your script must be executable (`chmod +x`).
- Running `/home/user/run_pipeline.sh` should execute the entire workflow from start to finish.
- Create the output directory `/home/user/logs/clean/` if it does not exist.
- You must use Bash for the main orchestration script (you can use standard Unix utilities like `sed`, `awk`, `grep`, `sort`, `uniq` within it).