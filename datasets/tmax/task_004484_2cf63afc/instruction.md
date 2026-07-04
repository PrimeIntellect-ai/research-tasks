You are a network engineer analyzing a captured traffic log that contains sensitive authentication tokens. You need to crack a captured authentication PIN, redact the sensitive tokens from the log file, and secure the output.

Perform the following steps:

1. **Brute-force the PIN (C Programming)**:
   You intercepted a hashing algorithm used for a 4-digit PIN (ranging from `0000` to `9999`). 
   The mathematical condition the correct PIN satisfies is: `(PIN * 12345) % 98765 == 61850`.
   Write a C program at `/home/user/crack.c` to brute-force and find the correct 4-digit PIN. 
   Save the cracked PIN (just the 4 digits) into `/home/user/cracked_pin.txt`.

2. **Sensitive Data Redaction**:
   The file `/home/user/traffic.log` contains raw HTTP requests. Some of these requests contain sensitive bearer tokens in the format `Authorization: Bearer <64-character-hex-string>`.
   Process `/home/user/traffic.log` and replace the 64-character hex strings with the exact word `REDACTED`. 
   For example, `Authorization: Bearer 1a2b...` should become `Authorization: Bearer REDACTED`.
   Save the cleaned output to `/home/user/redacted.log`.

3. **File Permissions**:
   To ensure the redacted log cannot be tampered with or read by unauthorized users, set the permissions of `/home/user/redacted.log` to be strictly read-only for the owner, and no permissions for group or others (i.e., `0400`).

Ensure all final files are exactly at the specified paths.