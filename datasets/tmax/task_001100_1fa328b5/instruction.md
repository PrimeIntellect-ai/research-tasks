You are acting as a compliance analyst for a financial institution. Your task is to generate clean, verified audit trails from raw system logs, ensuring no malicious payloads are stored in the final compliance records, and that all sensitive data is redacted.

There are three parts to this assignment:

1. **Audio Integrity Verification**:
   We received an audio recording of a stakeholder verifying the checksum of our raw logs archive. The file is located at `/app/audit_interview.wav`.
   - Transcribe or listen to this audio file to retrieve the spoken SHA-256 hash.
   - Verify that the archive `/app/logs.tar.gz` matches this hash.
   - Save the extracted hash (just the 64-character hex string) into `/home/user/archive_hash.txt`.

2. **Sensitive Data Redaction & Injection Defense**:
   Create a Bash script at `/home/user/filter_logs.sh` that takes a single file path as its argument and prints the processed output to `stdout`.
   The script must implement the following security rules on a line-by-line basis:
   - **XSS and Injection Filtering**: If a line contains any of the following substrings (case-insensitive), the script must completely DROP the line (do not print it):
     - `<script>`
     - `javascript:`
     - `onerror=`
     - `' OR 1=1`
     - `UNION SELECT`
   - **Data Redaction**: For all other lines, if the line contains a Social Security Number in the format `XXX-XX-XXXX` (where X is a digit), it must replace the digits with the literal string `XXX-XX-XXXX` (e.g., `123-45-6789` becomes `XXX-XX-XXXX`).
   - **Clean Lines**: Any line that does not trigger the injection filter and does not contain an SSN must be printed exactly as-is.

3. **Validation**:
   The automated compliance verifier will test your `/home/user/filter_logs.sh` script against an unseen dataset. It will pass files from a clean corpus and an evil corpus to your script.
   - You must ensure that safe log files are passed through without modification.
   - You must ensure that malicious lines are dropped and sensitive data is correctly redacted.

Constraints:
- Use only standard Bash built-ins, coreutils (like `grep`, `sed`, `awk`), and standard CLI tools.
- Your script must have execute permissions (`chmod +x /home/user/filter_logs.sh`).

Once you have verified the archive hash and created the script, you are done.