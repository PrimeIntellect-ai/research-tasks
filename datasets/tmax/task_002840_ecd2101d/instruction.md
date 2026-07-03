You are acting as a compliance analyst investigating a potential web server compromise. You have been provided with a suspicious binary found on one of the web nodes. Your objective is to extract hidden malicious configurations, decode them, prepare network policy mitigation scripts, and generate a standardized audit trail for compliance records.

Here are your instructions:

1. **Analyze the Binary:**
   You will find an ELF binary located at `/home/user/suspicious_web_worker.elf`. The attackers have hidden their Command and Control (C2) configuration inside a custom ELF section named `.malconf`. Extract the contents of this section. 

2. **Decode the Payload:**
   The extracted payload from the `.malconf` section is a Base64-encoded string. Once decoded, it will reveal a comma-separated list of malicious IP addresses.

3. **Generate Firewall Policies:**
   Create a bash script at `/home/user/block_ips.sh` that contains the necessary `iptables` commands to block incoming traffic from these IP addresses. 
   - The script must start with `#!/bin/bash`.
   - For each extracted IP address, add a rule to drop traffic on the INPUT chain (e.g., `iptables -A INPUT -s <IP> -j DROP`).
   - Make sure the script is executable (`chmod +x`).

4. **Generate the Audit Trail:**
   Create a JSON-formatted audit report at `/home/user/audit_report.json` containing the findings. The JSON must strictly adhere to the following structure:
   ```json
   {
     "elf_md5": "<MD5 checksum of the suspicious_web_worker.elf file>",
     "extracted_ips": [
       "<ip_1>",
       "<ip_2>",
       "..."
     ],
     "firewall_script": "/home/user/block_ips.sh"
   }
   ```
   *Note: Only the 32-character hex string should be in the `elf_md5` field. The `extracted_ips` must be a proper JSON array of strings.*

Complete these steps using standard command-line tools available in the terminal. Do not attempt to execute the firewall script, as you do not have root privileges; simply generating it correctly is sufficient.