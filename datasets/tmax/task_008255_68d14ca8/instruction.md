You are a DevSecOps engineer enforcing policy as code. A legacy application is logging sensitive credentials in an encrypted format, and you need to write a secure utility to redact these from the logs before they are ingested by the monitoring system.

Your task is to create a C program at `/home/user/redactor.c` that reads log data from `stdin`, brute-forces the weak encryption to verify the credential format, redacts the sensitive data, and writes the safe log to `stdout`.

Here are the specific requirements for `/home/user/redactor.c`:

1. **Process Isolation:** The very first thing your `main` function must do (after declaring variables) is enable strict seccomp mode using `prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT)`. This ensures the program can only use `read()`, `write()`, `_exit()`, and `sigreturn()` system calls, minimizing the blast radius if the log parser is exploited.
2. **Log Parsing & Decryption:** The program must read the input line by line. It should scan for the pattern `<SECRET:[hex_string]>`. 
3. **Brute-Force Verification:** The `[hex_string]` is an unknown 1-byte XOR encrypted string (represented as lowercase hexadecimal, e.g., `150416161a`). To ensure you are redacting actual credentials and not random binary data, you must brute-force the 256 possible 1-byte XOR keys. A credential is valid if, when decrypted, it begins with the exact string `PASS_`.
4. **Redaction:** If a `<SECRET:[hex_string]>` block contains a valid credential (starts with `PASS_` after decryption), replace the entire `<SECRET:...>` tag with the string `[REDACTED]` in the output. If it does not decrypt to a string starting with `PASS_` with any key, leave the tag unmodified.
5. **Standard Text:** Any text outside the `<SECRET:...>` tags should be passed through to `stdout` unmodified.

Once you have written the code, compile it into an executable at `/home/user/redactor`. 
Finally, use your executable to process the log file located at `/home/user/app_logs.txt` and save the output to `/home/user/safe_logs.txt`.

Ensure your C code is robust, correctly implements the strict seccomp sandbox, and accurately parses/replaces the text stream.