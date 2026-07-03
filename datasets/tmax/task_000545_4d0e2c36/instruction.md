You are acting as a forensics analyst investigating a compromised Linux host. A suspicious authentication wrapper script was found on the system, and evidence suggests an attacker successfully gained execution and leaked credentials by exploiting it.

We have collected two pieces of evidence for you in the `/home/user/evidence` directory:
1. `/home/user/evidence/auth_wrapper.sh`: A copy of the vulnerable Bash script used for authentication.
2. `/home/user/evidence/ps_dump.log`: A historical log of process executions (similar to `ps -eo pid,cmd`) captured during the suspected breach window.

Your task is to audit the script, find the vulnerability, and analyze the process dump to extract the attacker's payload.

Perform the following steps:
1. Identify the exact line number in `/home/user/evidence/auth_wrapper.sh` that contains an OS Command Injection vulnerability (CWE-78).
2. Analyze `/home/user/evidence/ps_dump.log` to locate the single execution where the attacker exploited this specific command injection vulnerability.
3. Extract the exact injected OS command used by the attacker in that execution (exclude the legitimate username and the semicolons used to chain the command).
4. The script accepts a Base64-encoded token as its second argument. Extract and decode the attacker's authentication token from the exploited process line.

Write your final findings to a log file located at `/home/user/forensics_report.txt` using exactly the following format (replace the bracketed placeholders with your findings):

```text
VULN_LINE=[Line number of the command injection vulnerability]
INJECTED_CMD=[The exact injected OS command, e.g., ls -la /]
DECODED_TOKEN=[The plaintext, decoded base64 token used by the attacker]
```

Constraints:
- Only report the core injected command (do not include the username, semicolons, or the base64 token in the INJECTED_CMD field).
- Ensure your `forensics_report.txt` precisely matches the key-value format requested.