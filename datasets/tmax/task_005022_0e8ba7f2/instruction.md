You are a DevSecOps engineer tasked with enforcing policy as code. You need to automate the processing of an encoded security audit log and verify a server certificate.

You have been provided with two files:
1. `/home/user/audit_log.b64`: A Base64-encoded text file containing a recent system execution log.
2. `/home/user/server.crt`: A standard X.509 TLS/SSL certificate.

Your task is to create a Rust program `/home/user/policy_checker.rs` (and run it to generate the final output) that does the following:
1. **Payload Decoding**: Read and decode the Base64 content from `/home/user/audit_log.b64`.
2. **Sensitive Data Redaction**: Scan the decoded text and replace any standard IPv4 addresses (e.g., `192.168.1.50`) with the exact string `[REDACTED_IP]`.
3. **Privilege Escalation Auditing**: Scan the decoded text for the exact substrings `sudo ` or `chmod 777`. If either is found anywhere in the log, the system must flag it.
4. Output the redacted log to a new file at `/home/user/processed_audit.log`.
5. If a privilege escalation risk (`sudo ` or `chmod 777`) was detected in step 3, append the exact line `WARNING: PRIVILEGE ESCALATION DETECTED` to the end of `/home/user/processed_audit.log`.

Finally, using standard Bash tools (`openssl`), extract the certificate Subject line from `/home/user/server.crt` (in the format `subject=...` or similar default OpenSSL output) and append it as the very last line of `/home/user/processed_audit.log`. 

The final `/home/user/processed_audit.log` must precisely match the decoded text (with IPs redacted), followed by the warning (if applicable), followed by the certificate subject line.

Compile your Rust program using `rustc` and run it, then run your bash commands to complete the log file.