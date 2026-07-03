You are a security engineer responding to an incident where a legacy C application is leaking credentials via command-line arguments, making them visible to any user on the system via `/proc`. Your task is to extract the encryption passphrase to access the historical process logs, reverse engineer the legacy binary to understand the leaked parameters, and write a C-based sanitization filter to redact these secrets from logs.

Step 1: Unpack the Corpus
An image from the incident report is located at `/app/incident_screenshot.png`. Use an OCR tool (like `tesseract`) to read the text in this image. It contains a critical master passphrase.
Use this passphrase to decrypt the GPG-encrypted process log corpus located at `/app/corpus.tar.gz.gpg`. Extract it to `/home/user/corpus/`. The archive contains two directories: `clean/` and `evil/`.

Step 2: Reverse Engineering
The legacy binary that leaked the credentials is at `/app/legacy_deployer`. Analyze this binary (using `strings`, `objdump`, or other tools) to identify the exact command-line argument flags it uses to accept sensitive passwords and authentication keys. There are exactly three distinct flags used for sensitive data. 

Step 3: Build the Redactor
Write a C program at `/home/user/redactor.c` and compile it to `/home/user/redactor`. 
Your program must:
- Read a command-line string from `stdin`.
- Parse the arguments (assume standard space separation; quotes will not be present in the simplified corpus).
- Identify any of the three sensitive flags discovered in Step 2.
- Replace the *value* immediately following the sensitive flag (or attached via `=`) with the literal string `[REDACTED]`.
- Print the resulting sanitized command line to `stdout`.

Constraints:
- Non-sensitive commands and arguments must remain completely unchanged.
- You must perfectly preserve the clean corpus while redacting the evil corpus.