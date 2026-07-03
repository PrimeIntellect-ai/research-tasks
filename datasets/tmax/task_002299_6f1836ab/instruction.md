You are a security auditor conducting service auditing and checking logs for leaked credentials and permissions issues. During an authentication flow test, you noticed that some web services and SSH wrappers might be logging highly sensitive information.

Your task is to create a Bash-based intrusion/leak detection script that scans log files and flags any sensitive data.

1. Write a script at `/home/user/detector.sh` that takes a single file path as its argument.
2. The script must scan the file and exit with code `1` (Reject) if it finds any of the following sensitive data, and exit with code `0` (Accept) if the file is clean.
   Target patterns to detect (using standard extended regular expressions):
   - **SSH Private Keys**: Any line containing `-----BEGIN ` followed by anything, followed by ` PRIVATE KEY-----`
   - **AWS Access Keys**: Any string matching `AKIA` followed by exactly 16 uppercase alphanumeric characters.
   - **Leaked Bearer Tokens**: Any string matching `Bearer ` (or URL-encoded `Bearer%20`) followed by an alphanumeric JWT-like string (letters, numbers, dashes, underscores, periods) of at least 20 characters.

To help you develop and test your script, we have provided two corpora of log files:
- `/app/corpus/clean/` : Contains normal service logs and port scanning outputs that MUST be accepted (exit code 0).
- `/app/corpus/evil/` : Contains logs with leaked sensitive data that MUST be rejected (exit code 1).

Additionally, the automated grading system relies on `bats-core` (Bash Automated Testing System) to verify your script. The source code for `bats-core` version 1.9.0 is vendored at `/app/bats-core`. However, a junior admin accidentally corrupted the main executable while auditing the server. 
You must locate the executable (`/app/bats-core/bin/bats`), find the deliberate perturbation (a broken shebang), and fix it so the verifier can run successfully.

Ensure your `detector.sh` script is executable (`chmod +x /home/user/detector.sh`).