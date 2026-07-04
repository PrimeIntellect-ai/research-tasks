You are tasked with building a Bash-based ETL pipeline for a Configuration Management (CM) system. The system produces a massive, continuous audit log of server state changes. Due to the sensitive nature of these logs, you must extract the relevant information, mask sensitive fields, and load the processed records into a database for safe auditing.

**Input:**
There is a raw log file located at `/home/user/cm_audit.log`. 
The log contains multi-line records formatted exactly as follows:
```
BEGIN_RECORD
TIMESTAMP: <ISO8601_Time>
ACTION: <Action_Name>
DETAILS: <Space_separated_key_value_pairs>
END_RECORD
```
Note: There may be empty lines or system warnings between records. You must only process data between `BEGIN_RECORD` and `END_RECORD` (inclusive).

**Requirements:**

1. **Information Extraction & Streaming:**
   Write a Bash script located at `/home/user/process_audit.sh`. The script must process `/home/user/cm_audit.log` as a stream (e.g., using `awk`, `sed`, or bash `while read` loops) without loading the entire file into memory at once.
   You need to extract the `TIMESTAMP`, `ACTION`, and `DETAILS` for each valid record.

2. **Data Masking:**
   The `DETAILS` field often contains sensitive information. You must apply the following masking rules *only* to the `DETAILS` string:
   - **Passwords:** Any key-value pair matching `password=<anything>` must be masked to `password=***`. (The value ends at the next space or end of line).
   - **IP Addresses:** Any key-value pair matching `ip=<octet1>.<octet2>.<octet3>.<octet4>` must have its last octet masked to `XXX`. For example, `ip=192.168.1.50` becomes `ip=192.168.1.XXX`.

3. **CSV Preparation:**
   Your streaming pipeline should convert the extracted, masked data into a comma-separated format (CSV). The output columns should strictly be:
   `timestamp,action,details`
   (Do not include a header row in the final output stream/file. Ensure fields do not contain literal commas, or quote them if they do).

4. **Database Bulk Load:**
   The script must automatically create an SQLite3 database at `/home/user/config_tracking.db` with the following table schema:
   `CREATE TABLE audit_log (timestamp TEXT, action TEXT, details TEXT);`
   The script must then bulk-import the transformed CSV data into this table. (Do this efficiently; e.g., using the `.import` command in sqlite3).

5. **Execution:**
   Ensure your script `/home/user/process_audit.sh` is executable and run it so that the database is fully populated by the end of your process. 

Your success will be verified by running SQL queries against `/home/user/config_tracking.db` to check row counts, masking correctness, and structured extraction.