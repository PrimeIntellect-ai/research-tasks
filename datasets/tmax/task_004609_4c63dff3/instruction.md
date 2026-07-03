You are a forensics analyst investigating a compromised Linux host. You have isolated a set of malware artifacts in `/home/user/investigation`. The malware acts as a local proxy, intercepting web traffic to downgrade Content Security Policies (CSP) and exfiltrating data to a Command & Control (C2) server. 

Your objectives are to reverse engineer the malware, test its authentication flow, and analyze the intercepted traffic logs to recover stolen evidence.

Perform the following steps:

1. **Reverse Engineering**: The attacker left behind a compiled Python bytecode file at `/home/user/investigation/c2_agent.pyc`. Analyze this file (e.g., using Python's `dis` module) to extract the hardcoded C2 authentication token.
2. **Authentication Flow Testing**: The malware communicated with a local staging server running on `http://127.0.0.1:8080`. Write a Python script to send a `GET` request to `http://127.0.0.1:8080/evidence`. You must include the extracted token in the `Authorization` header as a Bearer token. The server will respond with a JSON payload containing a `secret_flag`.
3. **Content Security Policy Analysis**: The directory contains a traffic log at `/home/user/investigation/traffic.json`. This file contains intercepted HTTP responses. The malware modifies the `Content-Security-Policy` header of specific domains to weaken them (specifically, by injecting `'unsafe-inline'` into the `script-src` directive, or removing the directive entirely). Identify all domains that had their CSP weakened by the malware.
4. **Reporting**: Create a final report at `/home/user/evidence_report.json` with the following exact structure:
```json
{
  "c2_token": "<extracted_token>",
  "secret_flag": "<flag_from_server>",
  "compromised_domains": ["<domain1>", "<domain2>"]
}
```
*Note: Sort the `compromised_domains` list alphabetically.*

Ensure you write a robust Python script to handle the authentication testing and data processing. Do not stop until `/home/user/evidence_report.json` is accurately populated.