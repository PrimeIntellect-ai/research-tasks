You are a security engineer tasked with rotating credentials and securing a legacy data processing pipeline. Recent audits revealed that an old database password was hardcoded and obfuscated in a process memory dump, and AWS access keys have been leaking into the application logs. 

You need to extract the old password, redact the leaked credentials, and create a secure execution wrapper for the new data pipeline.

Complete the following three phases:

**Phase 1: Sensitive Data Redaction**
An application log file exists at `/home/user/app.log`. It contains sensitive AWS Access Key IDs (which always start with `AKIA` followed by exactly 16 uppercase alphanumeric characters). 
Write a Bash script at `/home/user/redact.sh` that reads `/home/user/app.log` and replaces every instance of an AWS Access Key ID with the exact string `[REDACTED]`. The script should save the cleaned output to `/home/user/app_redacted.log`. Run your script to generate this file.

**Phase 2: Memory Dump Cryptanalysis**
A legacy service crashed and left a hex-encoded memory dump at `/home/user/mem.dmp`. We know the legacy system obfuscated the database password by applying a single-byte XOR cipher to the string. 
We also know the plaintext string begins exactly with `DB_PASS=`. 
Analyze the hex dump, determine the single-byte XOR key, decrypt the obfuscated string, and extract the password (the portion *after* `DB_PASS=`). 
Save the extracted plaintext password to a single file at `/home/user/recovered_pass.txt` (no trailing newlines).

**Phase 3: Process Isolation Wrapper**
You need to run a dummy processing script securely to verify the pipeline. 
Write a Bash script at `/home/user/run_secure.sh` that takes two arguments: a log file path and a password. 
The script must execute the pipeline script located at `/home/user/process.sh` with the following sandboxing restrictions:
1. It must run in a completely empty environment (using `env -i`), except for a single environment variable `SECRET_KEY` which should be set to the password provided as the second argument.
2. It must restrict the maximum number of open file descriptors to 50 for the executed process (using `ulimit`).
3. It must pass the log file path (the first argument) as the argument to `/home/user/process.sh`.

Finally, execute your wrapper script to process the redacted log with the recovered password:
`bash /home/user/run_secure.sh /home/user/app_redacted.log $(cat /home/user/recovered_pass.txt)`

(Note: You must create a dummy executable script at `/home/user/process.sh` that just echoes "Processing $1 with key $SECRET_KEY" to `/home/user/success.out` so you can verify it works, but the evaluation will focus on your wrapper script, the redacted log, and the recovered password).