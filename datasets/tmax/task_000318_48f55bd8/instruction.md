You are a security engineer performing a security audit and credential rotation for a legacy internal authentication service. 

Recently, we discovered that the service's token validation flow has a vulnerability conceptually similar to an "open redirect", but applied to the local filesystem (a path traversal vulnerability). This allows attackers to escalate privileges by reading arbitrary files on the system instead of the intended token files.

All files for this task are located in the directory `/home/user/cred_svc/`. Inside this directory, you will find:
1. `auth_helper.c`: The source code of the legacy token validation helper.
2. `auth_helper`: The compiled ELF binary of the helper.
3. `access.log`: The web server access log capturing token rotation requests.

Your task consists of three parts:
1. **ELF Analysis:** The previous developer hardcoded a backup credential key directly into the binary. Analyze the compiled `auth_helper` binary to extract this key. It is a string that starts with the prefix `BACKUP_`.
2. **Vulnerability Auditing:** Review the `auth_helper.c` source code. Identify the specific C function that is responsible for improperly constructing the file path without sanitizing user input, causing the path traversal vulnerability.
3. **Intrusion Detection:** Analyze the `access.log` file using pattern matching. Identify all unique IP addresses that attempted to exploit this path traversal vulnerability (i.e., any request where the token parameter contains `../`).

Finally, generate an audit report at exactly `/home/user/audit_report.json`. The file must be valid JSON with the following exact schema:
```json
{
  "hardcoded_key": "<the extracted BACKUP_ string>",
  "malicious_ips": ["<ip1>", "<ip2>", "..."],
  "vulnerable_function": "<name_of_the_vulnerable_C_function>"
}
```
*Note: The `malicious_ips` array should be sorted alphabetically/numerically as strings, and must only contain unique IPs.*