As an incident responder, you are investigating a potential breach on a Linux server. You have discovered a suspicious stripped executable located at `/app/telemetry_sender`. We suspect this tool is being used by an insider to exfiltrate credentials. By analyzing process execution logs (`/proc`), we noticed that the malicious actor passes sensitive internal tokens as command-line arguments to this binary, which then obfuscates them before transmitting.

To properly assess the impact of the breach and identify which tokens were compromised from captured network logs, we need a bit-exact Python replication of the obfuscation algorithm used by this binary.

Your task is to reverse-engineer the stripped ELF binary `/app/telemetry_sender`. You must analyze its execution and structure using standard Linux CLI tools to understand the custom cryptography/obfuscation routine it applies to its command-line argument. 

Once you understand the algorithm, write a Python script at `/home/user/emulator.py`. 
Your script must:
1. Accept exactly one command-line argument (the token string).
2. Apply the exact same obfuscation algorithm as `/app/telemetry_sender`.
3. Print the resulting obfuscated string to standard output, matching the original binary's output format perfectly (including any trailing newlines).

You must ensure that your Python script behaves identically to the binary for any alphanumeric input string. Automated verification will run hundreds of tests comparing the output of your Python script against the binary.