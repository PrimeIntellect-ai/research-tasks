You are an incident responder investigating a recent series of attacks on a web application. You have been provided with a web server access log, and your goal is to write a Go program to analyze the traffic, extract the exploit payloads, and generate mitigation configurations.

The access log is located at `/home/user/evidence/access.log`. 
Each line in the log follows this format:
`[TIMESTAMP] IP_ADDRESS HTTP_METHOD /path?payload=BASE64_STRING`

Your task is to write and execute a Go program at `/home/user/analyze.go` that does the following:
1. Reads `/home/user/evidence/access.log`.
2. Extracts and base64-decodes the `payload` parameter from each line.
3. Analyzes the decoded payload to determine if it is malicious. A payload is considered malicious if it contains either the substring `<script>` (indicating an XSS attack) or `cat /etc` (indicating command injection).
4. Creates a directory `/home/user/mitigation/` if it does not exist.
5. Writes all unique malicious decoded payloads (one per line) to `/home/user/mitigation/payloads.txt`.
6. Generates a shell script at `/home/user/mitigation/block_ips.sh` containing firewall rules to block the attacker IP addresses identified from the malicious log entries. The format for each line in the script should be exactly: `ufw deny from <IP_ADDRESS>`
7. Generates a Content Security Policy (CSP) header string to mitigate the XSS attacks, and writes it to `/home/user/mitigation/csp.txt`. The CSP must strictly contain exactly: `default-src 'self'; script-src 'self';`

After your Go program completes these tasks, you must use standard Linux commands to set the file permissions of `/home/user/mitigation/payloads.txt` to strictly read-only for the owner (0400), with no access for group or others, to prevent accidental execution of the forensic evidence.

Ensure your Go program compiles and runs successfully, and that all output files are correctly formatted and placed in the specified paths.