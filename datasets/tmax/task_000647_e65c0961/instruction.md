You are a forensics analyst recovering evidence from a compromised host. You have discovered a custom backdoor service and its associated log file. Your goal is to identify the attacker, understand their authentication mechanism, and prepare remediation steps.

The system contains the following evidence files:
1. `/home/user/suspicious.log`: Contains connection logs from the backdoor service.
2. `/home/user/auth_logic.c`: A recovered snippet of the backdoor's source code responsible for token validation.

Perform the following tasks:
1. **Log Parsing:** Analyze `/home/user/suspicious.log` to find the single IP address that successfully authenticated ("Auth success"). Note the "Seed" value provided in that log entry.
2. **Reverse Engineering & Token Generation:** Analyze the logic in `/home/user/auth_logic.c` to understand how the backdoor derives the valid access token from the seed. Write a C program at `/home/user/keygen.c` that accepts a seed as a command-line argument (as a base-10 integer) and prints the corresponding valid token (as an unsigned 32-bit base-10 integer) to standard output.
3. **Compilation:** Compile your C program to `/home/user/keygen`.
4. **Token Extraction:** Run your compiled `keygen` binary using the seed you found in the log file. Save the resulting token to `/home/user/attacker_token.txt`.
5. **Firewall Policy:** Create a shell script at `/home/user/block_attacker.sh` containing a single `iptables` command to block all incoming traffic from the attacker's IP address. The command must append a rule to the `INPUT` chain and `DROP` the traffic.

Ensure all requested files (`keygen.c`, `keygen`, `attacker_token.txt`, and `block_attacker.sh`) are placed in `/home/user/` with the exact specified names.