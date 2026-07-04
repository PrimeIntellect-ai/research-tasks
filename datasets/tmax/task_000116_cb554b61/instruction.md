You are an incident responder investigating a potential data breach. You have been provided with a server log file that contains sensitive Personally Identifiable Information (PII) mixed with routine system events. Your goal is to write a Rust tool to securely process this data for the investigation team.

You have the following files in `/app/`:
1. `/app/evidence_photo.png` - A photo of a physical note containing specific redaction rules for this incident.
2. `/app/raw_logs.txt` - The raw log file containing sensitive data.
3. `/app/raw_logs.txt.sha256` - The SHA-256 checksum of the raw log file.
4. `/app/server.crt` - The TLS certificate of the server from which the logs were extracted.

Your Rust program must perform the following tasks:
1. **File Integrity Verification:** Verify the SHA-256 hash of `/app/raw_logs.txt` matches the hash provided in `/app/raw_logs.txt.sha256`. If it does not match, the program must exit immediately with an error.
2. **TLS Certificate Management:** Parse the `/app/server.crt` certificate and extract the Subject's Common Name (CN).
3. **Sensitive Data Redaction:** Read the redaction rules from `/app/evidence_photo.png` (you may need to use OCR tools available on the system to read the image) and apply them to the contents of `/app/raw_logs.txt`. 
4. **Output Generation:** Write the processed data to `/home/user/redacted_logs.txt`.
   - The very first line of the output file must be exactly: `Server CN: <extracted_CN_here>`
   - The subsequent lines must be the redacted log entries, in the exact same order as the original file.

You must build and run your Rust program to generate `/home/user/redacted_logs.txt`. Your output will be evaluated by an automated script that computes the line-by-line accuracy against a perfectly redacted reference file. You must achieve an accuracy of at least 95% to pass.