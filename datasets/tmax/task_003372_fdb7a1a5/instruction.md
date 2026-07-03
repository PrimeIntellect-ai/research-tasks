You are an incident responder investigating a recent network intrusion. We have captured a suspicious binary dropped on one of our servers, along with a snippet of our web server's access logs. 

Your investigation steps:
1. Analyze the binary file located at `/home/user/suspicious.elf`. Embedded within this file is a configuration string formatted exactly as `C2_BEACON: <base64_string>`.
2. Extract the base64 string and decode it. The decoded string is a Regular Expression (regex) pattern used by the malware to identify its command-and-control beacon endpoints.
3. Parse the web server log file located at `/home/user/access.log`.
4. Use the decoded regex pattern to identify all malicious HTTP requests in the log file (match the regex against the request path/URI).
5. Extract the source IP addresses from the matching log entries.
6. Write the unique, numerically sorted IP addresses to a file located at `/home/user/compromised_ips.txt`. Each IP address should be on a new line.

Constraints & Notes:
- The log file follows a standard combined log format.
- Treat the decoded regex as an unanchored pattern unless it contains its own anchors.
- You may use any combination of shell commands, Python, or other scripting languages available in the terminal.