You are a forensics analyst responding to a compromised Linux host. You need to recover evidence from a web application directory to determine who attacked the system, what they did, and how they escalated privileges.

You have been provided with the following files in `/home/user/`:
1. `/home/user/app.py`: A backup of the vulnerable application code.
2. `/home/user/auth.log`: A log file containing a single suspicious authorization token left behind by the attacker.
3. `/home/user/priv_matrix.txt`: A dump of the system's `sudoers` configurations mapping users to their allowed privileged commands.

Your objectives:
1. **Code Auditing & Token Validation**: Audit `/home/user/app.py` to identify a critical security flaw (CWE-798: Use of Hard-coded Credentials). Use the discovered secret to decode and validate the token found in `/home/user/auth.log`. The token is a JSON Web Token (JWT) using the HS256 algorithm.
2. **Payload Decoding**: Extract the `username` and `payload` claims from the decoded token payload.
3. **Privilege Escalation Auditing**: Search `/home/user/priv_matrix.txt` for the extracted `username` to find the exact absolute path of the binary they are permitted to run with `NOPASSWD` as root.

Once you have gathered this information, generate a JSON report at `/home/user/forensics_report.json` with the exact following schema:

```json
{
  "attacker": "<extracted_username>",
  "payload": "<extracted_payload>",
  "escalation_binary": "<absolute_path_to_binary_from_priv_matrix>"
}
```

Ensure your output file is strictly valid JSON. You may use any language (Python, bash, etc.) to analyze the files and generate the report.