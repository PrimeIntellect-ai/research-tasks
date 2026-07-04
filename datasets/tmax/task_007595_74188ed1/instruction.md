You are acting as a security auditor for a Linux system. You have been tasked with identifying a compromised file based on permission vulnerabilities and integrity violations, and then generating a firewall mitigation script using Python.

The target directory is `/home/user/audit_target`. All files in this directory are meant to be strictly confidential and should only be accessible (read/write) by the owner (i.e., permission `600`). Any file with permissions granting access to 'group' or 'others' is considered a policy violation.

Additionally, a list of expected SHA256 hashes for all files in their original state is located at `/home/user/hashes.sha256`. 

A recent alert suggests one file was modified after its permissions were accidentally broadened. This compromised file contains a list of malicious IP addresses (one per line) appended by an attacker.

Your tasks are:
1. **Identify the compromised file**: Find the single file in `/home/user/audit_target` that BOTH violates the permission policy (is accessible by group or others) AND fails its integrity check against `/home/user/hashes.sha256`.
2. **Create an audit report**: Create a file at `/home/user/audit_report.txt` with exactly two lines containing the filename (just the name, not the path) and the actual (current) SHA256 hash of the compromised file.
   Format:
   ```
   COMPROMISED_FILE: <filename>
   ACTUAL_HASH: <current_sha256_hash>
   ```
3. **Write a mitigation script**: Write a Python script at `/home/user/generate_fw.py` that reads the compromised file, extracts all IPv4 addresses found in it (ignoring any non-IP text), and writes a bash script to `/home/user/firewall_rules.sh`.
4. **Generate the firewall rules**: Run your Python script so that `/home/user/firewall_rules.sh` is created. This bash script must contain `iptables` commands to drop incoming traffic from each extracted IP address.
   Format for each IP in `/home/user/firewall_rules.sh`:
   ```bash
   iptables -A INPUT -s <IP_ADDRESS> -j DROP
   ```

Make sure your Python script runs successfully and generates the correct `firewall_rules.sh` file. You do not need to execute the firewall script, as you do not have root privileges.