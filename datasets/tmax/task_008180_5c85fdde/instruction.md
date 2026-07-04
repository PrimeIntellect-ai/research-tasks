You are an incident responder tasked with investigating a potentially compromised Linux server. The system administrators suspect that a backdoor has been implanted in one of the custom background services, allowing unauthenticated remote access to sensitive data.

Your investigation must proceed through the following steps:

1. **File Integrity Verification:** 
   Navigate to `/home/user/services/`. This directory contains several ELF binaries that run on this server. You have been provided with a known-good baseline of SHA-256 hashes located at `/home/user/baseline_hashes.txt`. Verify the integrity of the binaries in the directory against this baseline to identify the *single* modified (compromised) binary.

2. **Binary and ELF Analysis:**
   Analyze the compromised ELF binary. This binary acts as a custom authentication daemon and runs continuously in the background. By inspecting the binary, you need to determine:
   - The specific TCP port it is listening on.
   - The backdoor mechanism. The attacker implemented a flawed authentication check heavily inspired by the "JWT `algorithm=none`" vulnerability. If a specific JSON-like string is passed in the payload, the service skips signature validation and returns the server's secret flag. 

3. **Exploitation and Validation (Python):**
   Write a Python script located at `/home/user/investigate.py` that connects to the compromised service via TCP and sends the correct payload to exploit the backdoor. Retrieve the secret flag from the service's response and save *only* the flag text to `/home/user/flag.txt`.

4. **Firewall Policy Remediation:**
   To contain the threat while the developers patch the binary, you must prepare a firewall rule. Create a bash script at `/home/user/firewall.sh` containing the exact `iptables` command an administrator would use to `DROP` all incoming TCP traffic destined for the compromised service's port. (Note: You do not have root privileges, so do not attempt to run the `iptables` command; just write it to the script). 
   The script must contain a single command in the format: `iptables -A INPUT -p tcp ... -j DROP`.

Constraints & Formatting:
- Do not kill or stop the background service. It is currently running and you must extract the flag from it.
- Your final flag must be written to `/home/user/flag.txt`.
- Your remediation script must be at `/home/user/firewall.sh`.