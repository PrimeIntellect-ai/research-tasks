You are a forensics analyst investigating a recently compromised web server. The attacker exploited a vulnerability in the login flow to redirect users maliciously, and then dropped a compiled binary beacon on the system to communicate with their Command and Control (C2) server. 

You need to perform a root cause analysis, extract the attacker's infrastructure details, draft a firewall rule to contain the beacon, and remediate the vulnerable code.

Here are your objectives:

1. **Vulnerability Identification & Remediation:**
   Review the Python Flask application located at `/home/user/webapp/app.py`. The attacker used a common vulnerability in the `/login` endpoint to perform a malicious redirect. 
   - Identify the standard MITRE CWE identifier for this vulnerability.
   - Modify `/home/user/webapp/app.py` to patch this vulnerability. Ensure that the `next` parameter is only followed if it is a relative path (it must start with a single `/` and must NOT start with `//` or `http`). If it is invalid, redirect to `/dashboard`.

2. **ELF Binary Analysis:**
   The attacker left a compiled executable at `/home/user/evidence/beacon`. 
   - Analyze this ELF binary to extract the hardcoded C2 IPv4 address. 

3. **Firewall Policy Drafting:**
   Since you do not have root privileges to apply firewall rules directly, you must draft the rule. Create a shell script at `/home/user/evidence/block_c2.sh` that contains exactly one `iptables` command. This command should append (`-A`) a rule to the `OUTPUT` chain to `DROP` all outbound `tcp` traffic destined for the extracted C2 IP address on destination port `4444`. 

4. **Forensics Report:**
   Generate a final report at `/home/user/evidence/report.json` with the following exact JSON structure:
   ```json
   {
       "cwe_id": "CWE-XXX",
       "c2_ip": "XXX.XXX.XXX.XXX"
   }
   ```
   (Replace `CWE-XXX` with the correct CWE ID for the open redirect vulnerability, and `XXX.XXX.XXX.XXX` with the extracted IP).