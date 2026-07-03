You are acting as a network security engineer investigating a potential open redirect vulnerability on a legacy web server. You have been provided with an audit package in `/home/user/audit/`.

Your tasks are to:

1. **Verify File Integrity:**
   Check the SHA256 integrity of the `/home/user/audit/server_config.tar.gz` file using its provided checksum file `/home/user/audit/server_config.tar.gz.sha256`. 
   As the first line of `/home/user/audit_report.txt`, write `INTEGRITY_OK` if the checksum matches, or `INTEGRITY_FAILED` if it does not.

2. **Audit Local Services:**
   The web server is currently running locally on a port somewhere between `8080` and `8090`. Scan localhost to find the open port.
   Append the result to `/home/user/audit_report.txt` as the second line in the format: `SERVER_PORT=<port>` (e.g., `SERVER_PORT=8080`).

3. **Analyze Traffic for Open Redirects:**
   The file `/home/user/audit/traffic.log` contains HTTP GET requests in the following format:
   `IP [timestamp] "GET /login?redirect=<url>&token=<token> HTTP/1.1" <status>`
   
   You must write a C program at `/home/user/analyzer.c` (and compile it to `/home/user/analyzer`) that reads this log file and identifies successful open redirect exploits.
   
   An exploit is considered successful if BOTH of the following conditions are met:
   - **External Redirect:** The `redirect` parameter starts with `http://` or `https://` (relative redirects like `/dashboard` are benign).
   - **Valid Token:** The `token` parameter is mathematically valid for the given `redirect` URL.

   **Token Validation Algorithm:**
   The expected token is a 2-character lowercase hex string. It is calculated by taking the sum of the ASCII values of all characters in the `redirect` URL, modulo 256, and then applying a bitwise XOR with `0x42`. 
   For example, if the redirect URL is `/`, the ASCII sum is 47. `47 % 256 = 47`. `47 ^ 0x42 = 25`. The hex representation of 25 is `19`.
   
   For each successful open redirect exploit found in the log, your C program (or a shell command utilizing it) must append the attacker's IP address to `/home/user/audit_report.txt` in the format: `EXPLOIT_IP=<ip>`.

Ensure that the final output file `/home/user/audit_report.txt` is strictly formatted as requested.