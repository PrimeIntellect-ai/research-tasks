You are an incident responder investigating a suspected privilege escalation on a Linux server. The system administrators found a suspicious binary that appears to act as a custom authentication helper, which they believe the attacker used to gain root access. 

You have been provided with an archive of the incident data, but for this exercise, the relevant files have been extracted to `/home/user/incident/`.

Inside `/home/user/incident/`, you will find:
1. `auth.log` - A snippet of the system's authentication logs from the time of the breach.
2. `auth_helper.c` - The source code of the suspicious binary found on the system (which was compiled and deployed with the setuid bit set).

Your task is to:
1. Parse `auth.log` to identify the attacker's username and IP address. The attacker successfully escalated privileges using the custom `auth_helper`.
2. Analyze the `auth_helper.c` source code. Understand the custom checksum/token validation logic it uses.
3. Based on the logs and the C code, determine the exact checksum value the attacker targeted.
4. Craft a valid plaintext token that successfully bypasses the authentication check in `auth_helper.c`.
5. Output your findings in a strictly formatted JSON file at `/home/user/findings.json`.

The `/home/user/findings.json` file must contain exactly these keys:
```json
{
  "attacker_ip": "<extracted IP>",
  "attacker_user": "<extracted username>",
  "valid_token": "<your crafted plaintext token>"
}
```

Constraints:
- Do not modify the original `auth.log` or `auth_helper.c` files.
- You may compile `auth_helper.c` to test your crafted token.