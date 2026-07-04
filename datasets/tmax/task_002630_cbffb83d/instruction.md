You are a network security engineer investigating a potentially compromised internal Go web service. The server is currently running locally on the machine, but the exact port is undocumented. You have been provided with the source code of the service and a recent traffic log.

Your objectives are to audit the running service, analyze the source code for vulnerabilities, test the authentication mechanism, and process the traffic logs to identify the attackers.

Perform the following steps:

1. **Service Auditing:** Determine which port the undocumented Go service (process name `goserver`) is listening on. Write the port number to `/home/user/port.txt`.

2. **Vulnerability Analysis & Authentication Testing:** Review the source code located at `/home/user/app/server.go`. The application has a `/login` endpoint and a `/search` endpoint. 
    - Identify the specific SQL injection vulnerability in the authentication flow.
    - Identify the Cross-Site Scripting (XSS) vulnerability in the search flow.
    - You may use `curl` to test the running service to confirm your findings.

3. **Data Processing:** The file `/home/user/app/traffic.log` contains JSON-formatted access logs from the past 24 hours. Write a Go program at `/home/user/process_logs.go` that reads this log file and extracts the IP addresses of any clients that attempted *either*:
    - The SQL injection bypass on the `/login` endpoint (look for payloads containing the exact string `' OR 1=1 --`).
    - An XSS attack on the `/search` endpoint (look for payloads containing `<script>`).

4. **Execution:** Run your Go program. Have it output the unique, deduplicated attacker IP addresses, sorted in ascending order, one per line, to the file `/home/user/attacker_ips.txt`.

Constraints:
- Only use standard Bash utilities and the Go toolchain.
- The logs are in JSON format, with fields: `ip`, `method`, `path`, and `status`. Ensure your Go code correctly parses the JSON lines.