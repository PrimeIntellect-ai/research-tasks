You are a security auditor investigating a potential backdoor in a custom network utility. 

You have been provided with a compiled ELF binary located at `/home/user/bin/network-diagnostic`. This binary is suspected to contain a hardcoded secret key used to validate backdoor access tokens.

Additionally, you have access to the service logs located at `/home/user/logs/auth.log`. The malicious actor has been using the backdoor, leaving traces in this log file.

Your task is to:
1. Analyze the ELF binary `/home/user/bin/network-diagnostic` to extract the hardcoded secret key. The key is stored as a string prefixed with `__AUTH_KEY_V2__=`.
2. Determine the valid backdoor token. The token is expected to be a SHA256 hex digest of the secret key concatenated with the string `"system_auditor"`. (e.g., `hash(secret_key + "system_auditor")`). Write a Python script to compute this.
3. Analyze the `/home/user/logs/auth.log` file using pattern matching to identify all unique IP addresses that successfully authenticated using the backdoor. Successful backdoor authentications are logged with the exact phrase: `Successful diagnostic override from IP: <IP_ADDRESS>`.
4. Generate a final report in JSON format at `/home/user/audit_report.json`.

The JSON file must have the following exact structure:
```json
{
  "extracted_key": "<the secret key without the prefix>",
  "valid_token": "<the computed SHA256 hex digest>",
  "compromised_ips": [
    "<ip_1>",
    "<ip_2>"
  ]
}
```
Note: Sort the `compromised_ips` list in ascending alphabetical/string order.