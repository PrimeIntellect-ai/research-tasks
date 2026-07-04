You are a network engineer analyzing traffic and authentication anomalies on a Linux server. 

You have been provided with an authentication log file at `/home/user/auth_log.txt` and a password wordlist at `/home/user/wordlist.txt`. 

Your task is to analyze these files and perform the following actions:
1. **Identify the Attacker:** Parse `/home/user/auth_log.txt` to find the IP address that has the highest number of "Failed login" attempts. Write ONLY this IP address to `/home/user/top_attacker.txt`.
2. **Crack the Admin Password:** The log file also contains a "Successful login" entry for the user `admin` along with the MD5 hash of their password. Extract this hash and use the wordlist at `/home/user/wordlist.txt` to crack the password. Write the plaintext password to `/home/user/admin_pass.txt`.
3. **Generate Firewall Rule:** Write a Python script at `/home/user/generate_fw.py` that reads the IP address from `/home/user/top_attacker.txt` and prints out the exact `iptables` command to drop all incoming traffic from that IP address. The command format must be `iptables -A INPUT -s <IP> -j DROP`. Run your script and redirect its output to `/home/user/fw_rule.txt`.

Ensure your final outputs are exactly as requested, containing no extra spaces or newlines.