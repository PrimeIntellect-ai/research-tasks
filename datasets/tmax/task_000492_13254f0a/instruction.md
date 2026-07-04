You are a security engineer tasked with rotating credentials for an older internal C++ FastCGI application and preparing its replacement for deployment. The old version leaked its API key, and you need to perform an audit and cleanup.

Your working directory is `/home/user`.

Here are the resources at your disposal:
1. `/home/user/app/old_auth.bin`: The legacy compiled C++ ELF binary. The old API key (starting with `sk_live_`) is hardcoded inside this binary.
2. `/home/user/logs/access.log`: The web server access logs. The old API key was accidentally leaked in plaintext in these logs.
3. `/home/user/app/new_auth.cpp`: The source code for the next generation of the application. It correctly reads the API key from environment variables, but it contains a glaring web security vulnerability related to how it echoes user input to the browser.

Perform the following tasks using standard bash commands and utilities:

1. **Extract and Hash the Key**: Analyze the legacy binary `old_auth.bin` to extract the old hardcoded API key. Compute the SHA-256 hash of the exact key string (no trailing newlines) and write it to `/home/user/rotation_report.txt` in the format: `OLD_KEY_HASH=<hash>`.
2. **Data Redaction**: Clean the `/home/user/logs/access.log` file in place. Replace every instance of the old API key with the exact literal string `[REDACTED]`. The rest of the log lines must remain unchanged.
3. **Vulnerability Analysis**: Audit `new_auth.cpp` to identify the primary web security vulnerability present in the code. Determine its standard CWE identifier (e.g., CWE-89, CWE-79, CWE-22) and append it to `/home/user/rotation_report.txt` in the format: `NEW_CODE_CWE=<CWE-ID>`.

The final state must have the `rotation_report.txt` file populated with exactly two lines, and the `access.log` file properly sanitized.