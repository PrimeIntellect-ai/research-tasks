You are a DevSecOps engineer enforcing "Policy as Code." Your organization wants to automate the auditing of local configuration files and user credentials without relying on third-party SaaS tools.

You must write a Python test suite named `/home/user/policy_tester.py` that analyzes an SSH configuration, a firewall export, and a shadow file. The script must execute the checks and output a precise JSON report.

**Task Requirements:**

1. **Environment Preparation:**
   - Install any Python dependencies you might need (e.g., `passlib` for password hashing) into your user environment using `pip`.

2. **SSH Hardening Check:**
   - **Input:** Parse the file at `/home/user/sshd_config_test`.
   - **Policy:** 
     - `PermitRootLogin` must be explicitly set to `no`.
     - `PasswordAuthentication` must be explicitly set to `no`.
   - **Action:** If either setting is missing, commented out, or set to anything other than `no`, record the name of the setting as a violation.

3. **Firewall Policy Check:**
   - **Input:** Parse the file at `/home/user/iptables_export.txt`. This file contains the output of `iptables -S`.
   - **Policy:**
     - The default policy for the `INPUT` chain must be `DROP` (i.e., `-P INPUT DROP`).
     - Only TCP port 22 is allowed for incoming traffic (`-A INPUT -p tcp ... --dport 22 -j ACCEPT`).
   - **Action:** 
     - If the `INPUT` default policy is not `DROP`, record the violation exactly as: `"INPUT policy is not DROP"`
     - If any other destination port (e.g., 80, 8080) is accepted in the `INPUT` chain, record the violation exactly as: `"Unauthorized port <PORT> ACCEPT"` (replace `<PORT>` with the actual port number found).

4. **Credential Audit (Password Cracking):**
   - **Input:** Parse `/home/user/shadow_test` (standard Linux shadow file format) and `/home/user/wordlist.txt`.
   - **Policy:** No user should have a password that exists in the provided wordlist.
   - **Action:** Perform a dictionary attack on the hashes in `shadow_test` using the words in `wordlist.txt`. Record the usernames of any accounts whose passwords are successfully cracked.

5. **Output Generation:**
   - Your script must run the audit and save the results to exactly `/home/user/audit_report.json`.
   - The JSON file must have exactly this structure and keys (arrays can be empty if there are no violations, but must be sorted alphabetically):
     ```json
     {
       "ssh_violations": ["PasswordAuthentication", "PermitRootLogin"],
       "firewall_violations": ["INPUT policy is not DROP", "Unauthorized port 8080 ACCEPT"],
       "compromised_users": ["appuser", "dev"]
     }
     ```

Write and execute `/home/user/policy_tester.py` so that it reads the input files, performs the analysis, and successfully generates `/home/user/audit_report.json`.