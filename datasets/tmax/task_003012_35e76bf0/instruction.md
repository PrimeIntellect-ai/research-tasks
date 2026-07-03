You are an incident responder investigating a series of suspicious SSH login attempts on a Linux server. The system owner has provided you with an extract of the authentication logs and the current SSH daemon configuration file. You need to analyze the logs algorithmically using C, generate remediation scripts, and provide a hardened SSH configuration.

You do not have root access, so you will place all your remediation artifacts in a specific directory.

Here is the setup:
- Log file: `/home/user/logs/auth.log`
- Current SSH config: `/home/user/logs/sshd_config_old`
- Output directory: `/home/user/remediation` (you must create this directory)

Perform the following tasks:
1. Create the `/home/user/remediation` directory.
2. Write a C program at `/home/user/analyze_logs.c` that reads `/home/user/logs/auth.log`. The program must count the number of "Failed password" attempts for each IP address. If an IP address has strictly more than 3 failed attempts, write that IP address (one per line) to `/home/user/remediation/blocked_ips.txt`.
3. Compile and execute your C program to generate `blocked_ips.txt`.
4. Based on the IPs in `blocked_ips.txt`, generate a shell script at `/home/user/remediation/block.sh` that contains the firewall commands to block these IPs. For each IP, add a line with the exact format: `iptables -A INPUT -s <IP> -j DROP`.
5. Copy the provided `/home/user/logs/sshd_config_old` to `/home/user/remediation/sshd_config_secure`. Modify `sshd_config_secure` to harden it: specifically, ensure that `PermitRootLogin` is set to `no` and `PasswordAuthentication` is set to `no`. Ensure any existing contradictory lines are removed or commented out.

Your final artifacts must be exactly at:
- `/home/user/remediation/blocked_ips.txt`
- `/home/user/remediation/block.sh`
- `/home/user/remediation/sshd_config_secure`