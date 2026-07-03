You are an incident responder investigating a potentially compromised Linux server. Since you are operating in a restricted triage environment, you must use standard Bash tools (coreutils, grep, awk, sed, strings, etc.) to analyze the artifacts collected from the system.

The artifacts are located in the `/home/user/investigation/` directory.

Your task is to write a Bash script at `/home/user/investigate.sh` that automates the analysis of these artifacts and generates a summary report. Your script must perform the following steps:

1. **Service Auditing**: Parse the simulated socket statistics file `/home/user/investigation/ss_output.txt` to find the PID of the rogue process named exactly `backdoor`.
2. **Reverse Engineering**: Analyze the binary artifact `/home/user/investigation/backdoor_bin`. Use basic binary string extraction to find the hardcoded Command and Control (C2) URL. The malicious URL always starts with `https://` and ends with `.evil.com/payload`.
3. **Intrusion Detection (Pattern Matching)**: Scan the web server access logs at `/home/user/investigation/access.log`. Identify all unique IP addresses that attempted a Log4j-style exploit (look for request URIs containing the string `jndi:ldap`).
4. **Content Security Policy (CSP) Enforcement Auditing**: Analyze the web application's header configuration in `/home/user/investigation/csp.txt`. Extract all external domains/URLs explicitly allowed by the `script-src` directive. Ignore keywords like `'self'` or `'unsafe-inline'`; extract only the actual external URLs (e.g., `https://trusted.cdn.com`).

Your script must execute these steps and output the findings to `/home/user/report.txt` in the following exact format:
```
BACKDOOR_PID=[Extracted PID]
C2_URL=[Extracted URL]
ATTACKER_IPS=[Comma-separated list of unique IPs, sorted alphabetically]
ALLOWED_SCRIPTS=[Comma-separated list of allowed script-src URLs, sorted alphabetically]
```

Example of expected output format in `/home/user/report.txt`:
```
BACKDOOR_PID=1234
C2_URL=https://example.evil.com/payload
ATTACKER_IPS=10.0.0.1,192.168.1.5
ALLOWED_SCRIPTS=https://analytics.com,https://cdn.example.com
```

Once you have written `/home/user/investigate.sh`, run it so that `/home/user/report.txt` is created with the correct data. Ensure your script handles the file parsing robustly using Bash utilities.