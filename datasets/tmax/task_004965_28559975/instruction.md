As a compliance analyst, you are tasked with processing sensitive audit trails and hardening our server configurations. 

Follow these steps to complete your task:

1. **Information Extraction**: A scanned memo is located at `/app/memo.png`. Use OCR or visual inspection to extract the password written on it. 
2. **Archive Decryption**: Use the extracted password to unzip `/home/user/audit_archive.zip`.
3. **Data Redaction Optimization**: Inside the archive, you will find `redact.cpp` and a small sample log `sample.log`. The C++ program redacts 16-digit credit card numbers (which may be separated by dashes or spaces, e.g., `1234-5678-9012-3456` or `1234 5678 9012 3456` or `1234567890123456`) by replacing the entire matched string with `[REDACTED]`. The current implementation uses `std::regex` and is far too slow for our multi-gigabyte production logs. 
   - Rewrite the core logic in `redact.cpp` without using heavy regex, employing a fast manual character-scanning approach or state machine.
   - Compile your optimized code to `/home/user/redactor`. It must accept two arguments: `<input_file>` and `<output_file>`.
4. **SSH Hardening**: You have been provided a configuration file at `/home/user/sshd_config`. Modify it to disable `PermitRootLogin` and `PasswordAuthentication` to meet our compliance standards.
5. **Integrity Verification**: Generate a SHA256 checksum of your compiled `/home/user/redactor` binary and save the output (just the hash and filename) to `/home/user/integrity.sha256`.

Your C++ implementation will be evaluated against a massive hidden log file. To pass, your program must produce the exact correct redacted output while executing faster than the strict metric threshold.