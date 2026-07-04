You are an incident responder investigating a compromised server. You have discovered a suspicious file upload handler and a log of payloads sent to it by an attacker. 

The server has the following files:
1. `/home/user/upload_handler.py` - The script the attacker was targeting. It receives Base64-encoded JSON payloads, decrypts the `content` field, and saves it to a file specified by the `filename` field. 
2. `/home/user/incident_logs.txt` - A log file containing the attacker's payloads. Each line is a Base64-encoded JSON object.

Your analysis reveals that `upload_handler.py` is susceptible to a path traversal vulnerability. 

Your task is to write a script (in any language of your choice) to process the attacker's payloads and generate an incident report. You must:

1. **Decode and Decrypt**: Read each line from `/home/user/incident_logs.txt`. Base64-decode the line to get a JSON object. The JSON has `filename` and `content` fields. The `content` is hex-encoded and encrypted using the same XOR cipher and key found in `/home/user/upload_handler.py`. Decrypt it to plain text.
2. **Vulnerability Analysis**: Determine if the `filename` indicates a path traversal attack. A payload is considered a path traversal attack if the `filename` contains the substring `../`.
3. **Sensitive Data Redaction**: The attacker may have uploaded stolen data. Scan the decrypted plaintext content for US Social Security Numbers (format: `XXX-XX-XXXX`, where `X` is a digit). Replace any found SSN entirely with the exact string `[REDACTED]`.
4. **Reporting**: Create a JSON report at `/home/user/ir_report.json`. The file must contain a single JSON array of objects, one for each payload in the same order as the log file. Each object must have the following keys:
   - `filename` (string): The exact `filename` value from the original payload.
   - `is_traversal` (boolean): `true` if it's a path traversal attack, `false` otherwise.
   - `redacted_content` (string): The decrypted plaintext content with all SSNs replaced by `[REDACTED]`.

Ensure your script handles the file reading, decoding, decrypting, redaction, and reporting accurately.