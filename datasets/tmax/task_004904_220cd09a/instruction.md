You are a forensics analyst investigating a compromised host. The attacker managed to breach a local Python web application and left behind several artifacts in the `/home/user/investigation` directory.

Your objective is to analyze the artifacts and generate a forensic report in JSON format. 

Perform the following tasks:
1. **Reverse Engineering:** The attacker left a compiled Python payload at `/home/user/investigation/payload.pyc`. Reverse engineer or disassemble this file to extract two key pieces of information:
   - The `exfiltration_ip` (an IP address hardcoded in the script).
   - The `malicious_csp` (a Content Security Policy string injected by the attacker to bypass our restrictions).
2. **Network Policy Auditing:** The attacker modified the local firewall to redirect traffic from our web service (port 8080) to their own listener. Analyze `/home/user/investigation/iptables_dump.txt` to determine the `redirected_port` (integer) the attacker used.
3. **Privilege Escalation Auditing:** The attacker left a backdoor binary with the SUID bit set in the `/home/user/investigation/bin` directory. Identify the name of this binary (`suid_binary`).

Once you have gathered all this information, create a file at `/home/user/investigation/report.json` with the following precise JSON structure:

```json
{
  "exfiltration_ip": "<extracted IP>",
  "malicious_csp": "<extracted CSP string>",
  "redirected_port": <integer port>,
  "suid_binary": "<name of the SUID file>"
}
```

Make sure all keys match exactly, and the file is valid JSON. Use Python and standard Linux tools to complete your investigation.