As a forensics analyst, you are investigating a compromised host. We found an intercepted audio recording at `/app/voicemail.wav` left by the attackers. It contains the name of a highly sensitive project they were targeting.

We know the attackers deployed a log redaction script to hide their exfiltration of this project and other sensitive data, as well as to mask their SQL injection attempts. We managed to recover the requirements for their redaction script but not the script itself. 

You must recreate their log processing script exactly so we can understand how they manipulated the system logs. Write a Python 3 script at `/home/user/redactor.py` that reads text from `stdin` line by line and writes the processed text to `stdout`.

The script must process each line independently and apply the following transformations in order:
1. **Sensitive Data Redaction (CC)**: Identify any 16-digit credit card numbers (a sequence of exactly 16 digits bounded by non-digits or line start/end) and replace them with `[REDACTED_CC]`.
2. **Sensitive Data Redaction (Project)**: Listen to `/app/voicemail.wav` to identify the secret project name. The audio will mention a single specific capitalized word as the project name. Replace all exact case-sensitive occurrences of this project name with `[REDACTED_PROJECT]`.
3. **CWE Identification**: If the line contains the exact SQL injection payload `' OR 1=1 --` (indicating an attempt to exploit CWE-89), append the exact string ` [CWE-89_DETECTED]` to the very end of the line (immediately before the newline character).

Requirements:
- The script must handle streaming input efficiently and terminate when stdin is closed.
- Do not add any extra blank lines or modify the original newlines, except to insert the CWE warning just before the newline of the affected line.
- The script must be perfectly deterministic and match our reference behavior bit-for-bit.