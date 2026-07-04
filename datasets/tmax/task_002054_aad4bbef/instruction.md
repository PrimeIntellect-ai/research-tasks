You are a penetration tester analyzing a system for sensitive credential leakage via process arguments (which can be exposed in `/proc` or system logs).

We captured a screenshot of the Intrusion Detection System (IDS) dashboard during a suspected breach. The image is located at `/app/dashboard.png`. 

Your tasks are as follows:
1. Extract the exact token prefix and the format of the leaked credentials from the dashboard image. (You may use `tesseract` or other available tools to read the image).
2. We have provided a large simulated process execution log at `/app/process_events.log`. This file contains millions of characters of logged command lines.
3. Write a Bash script at `/home/user/redact.sh` that reads `/app/process_events.log` and redacts all instances of the leaked tokens that match the format specified in the image.
4. When redacting, replace the sensitive payload (the characters following the prefix) with exactly `[REDACTED]`. Do not alter the prefix itself, and do not redact tokens that do not match the specific prefix and length/character set constraints shown in the dashboard.
5. Run your script and save the output to `/home/user/redacted_events.log`.

Your solution will be evaluated by an automated metrics verifier that compares `/home/user/redacted_events.log` against a hidden ground-truth file. You must achieve a line-by-line redaction accuracy of 0.99 (99%) or higher. 

Ensure your script is executable (`chmod +x /home/user/redact.sh`) and uses standard bash tools like `sed`, `awk`, or `grep`.