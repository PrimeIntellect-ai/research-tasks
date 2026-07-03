You are a compliance analyst assigned to generate an audit trail for a legacy system that has suspected tampering. You have been provided with a raw system log, a file integrity manifest, and a legacy binary tool used by the system administrators. 

Your objective is to extract critical encrypted events, decrypt them by reverse-engineering the legacy tool for its secret key, verify system file integrity, and output a final compliance report.

Here are the resources in your environment:
1. `/home/user/syslog.dat`: A log file containing various system events. Some critical events contain encrypted payloads.
2. `/home/user/sec_tool`: A compiled Linux ELF binary historically used to encrypt the logs. The source code is lost. It is known to use AES-256-CBC for encryption, using a hardcoded password stored somewhere within the binary.
3. `/home/user/manifest.sha256`: A standard SHA256 checksum file covering three configuration files located in `/home/user/conf/`. One of these configuration files has been tampered with and will fail the checksum validation.

Perform the following tasks using Bash:
1. Parse `/home/user/syslog.dat` for all lines containing the string `CRITICAL_ERROR`. Extract the base64-encoded encrypted payload which appears after the prefix `Payload: ` on those lines.
2. Analyze the `/home/user/sec_tool` binary to recover the hardcoded encryption password.
3. Decrypt the extracted payloads using `openssl enc -aes-256-cbc -d -a -pbkdf2 -pass pass:<RECOVERED_PASSWORD>`.
4. Verify the integrity of the files in `/home/user/conf/` using `/home/user/manifest.sha256`. Identify the absolute path of the file that fails the check.
5. Generate a final report at `/home/user/audit_report.txt` with the following strict format:

```
[Decrypted Events]
<Insert the decrypted string from the first CRITICAL_ERROR log>
<Insert the decrypted string from the second CRITICAL_ERROR log>

[Tampered File]
<Insert the absolute path of the file that failed the integrity check>
```

Note: Maintain the exact order of the decrypted events as they appear in the log file. Ensure no extra spaces or trailing lines are added to the decrypted strings in the report.