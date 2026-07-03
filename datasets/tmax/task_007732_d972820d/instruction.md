I am a compliance analyst working on generating audit trails and automated network isolation policies for a set of internal applications. We have a batch of pre-compiled ELF binaries in the `/home/user/binaries` directory. Our compliance policy strictly mandates that no binary should have an executable stack (the NX bit must be enforced). 

Some of these binaries violate this policy and contain hardcoded external IPv4 addresses that they communicate with. I need you to create a Bash script at `/home/user/audit_scanner.sh` that automates the vulnerability scanning, extracts the network indicators, and generates a firewall configuration script.

Your script must perform the following actions when executed:
1. Iterate over all files in `/home/user/binaries/`.
2. Analyze the ELF headers of each binary to determine if it has an executable stack (i.e., missing NX protection, where the `GNU_STACK` segment is executable).
3. For every vulnerable binary found, extract the embedded IPv4 address (you can assume there is exactly one IPv4 address string present in the vulnerable binaries).
4. Append an entry to an audit log located at `/home/user/audit_trail.log`. The format for each vulnerable binary must be exactly:
   `VULNERABLE_BINARY:<filename>,BLOCKED_IP:<ip_address>`
   (Sort the output alphabetically by filename before writing to the log to ensure consistent ordering).
5. Generate an iptables shell script at `/home/user/block_ips.sh` that drops all outbound traffic to the extracted IPs. For each vulnerable IP, the script should contain exactly this command:
   `iptables -A OUTPUT -d <ip_address> -j DROP`
   Add `#!/bin/bash` as the first line of this script.

Run your script once it is created so the output files are generated for my review. Ensure both `/home/user/audit_trail.log` and `/home/user/block_ips.sh` are created and contain the correct compliance artifacts.