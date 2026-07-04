You are acting as a security engineer responding to a severe credential leakage incident. 

We suspect that a custom legacy credential rotation binary, used by our system administrators, has been leaking temporary authentication tokens via command-line arguments. Because command-line arguments are visible in `/proc`, our system monitoring agents have inadvertently captured these secrets in our process logs.

We have a forensic package for you to analyze.
1. We intercepted a voicemail from a system administrator where they state the master password for the forensic archive. The audio is located at `/app/voicemail.wav`. You will need to transcribe this audio to recover the password.
2. Use the transcribed password to extract the encrypted archive located at `/app/evidence.zip`.
3. Inside the archive, you will find two files:
   - `rotator_elf`: The legacy compiled binary that performs the credential rotation. 
   - `process_logs.txt`: A large file containing historical `ps aux` snapshots.
4. Perform binary analysis on `rotator_elf` to determine the exact format, prefix, or regex pattern of the authentication tokens it generated and passed via command line.
5. Write a Python script to parse `process_logs.txt` and redact all leaked tokens that match the pattern you found in the binary. Replace the actual token values with the exact string `[REDACTED]`. Leave the rest of the log lines unchanged.
6. Save the fully redacted log file to `/home/user/redacted_logs.txt`.
7. Ensure that your Python script and the final log file have restrictive permissions (0600) so that only the owner can read them, following the principle of least privilege.

The automated verification system will compute the F1 score of your redactions against a secret ground-truth file. Your redacted log must achieve an F1 score of >= 0.99 to pass.