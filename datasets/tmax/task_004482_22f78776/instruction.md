You are an incident responder and forensics analyst investigating a recently compromised web server. The attacker managed to exfiltrate sensitive user data via an SQL injection vulnerability. 

You have been provided with two pieces of evidence left on the compromised host:
1. The web server access log: `/home/user/access.log`
2. A raw data dump left by the attacker in a hidden directory: `/home/user/compromised_db_dump.csv`

Your task is to analyze the logs, identify the attacker, and safely prepare the exfiltrated data for legal evidence by redacting sensitive Personally Identifiable Information (PII).

Perform the following steps using standard Linux command-line tools:

1. **Log Analysis and Correlation**:
   Analyze `/home/user/access.log`. The log contains normal traffic and several malicious attempts. Identify the IP address and the exact timestamp of the **successful** SQL injection attack. 
   * A successful attack will have an HTTP status code of `200`.
   * The SQL injection payload will be visible in the request URI (look for standard SQLi keywords like `UNION`, `SELECT`).

2. **Sensitive Data Redaction**:
   The file `/home/user/compromised_db_dump.csv` contains the exfiltrated user data with columns: `id,name,email,ssn,cc_number`.
   You must create a redacted version of this file at `/home/user/redacted_evidence.csv`.
   * Replace all Social Security Numbers (format: `ddd-dd-dddd`, where `d` is a digit) with `XXX-XX-XXXX`.
   * Replace all Credit Card Numbers (format: `dddd-dddd-dddd-dddd`) with `XXXX-XXXX-XXXX-XXXX`.
   * The header and all other data must remain unchanged.

3. **Forensics Report Creation**:
   Create a summary report at `/home/user/forensics_report.txt` with exactly the following format:

   ```
   Attacker IP: [Insert Attacker IP here]
   Attack Timestamp: [Insert Timestamp here, e.g., 10/Oct/2023:13:55:36 +0000]
   Redacted Records: [Insert the total number of data rows redacted, excluding the header]
   ```

Make sure your redacted CSV is correctly formatted and your report exactly matches the required keys and structure.