You are a security compliance analyst conducting an incident response audit on a compromised server. You need to trace a series of brute-force attacks, crack the weak passwords used by the victims, and identify unauthorized backdoors left by the attackers. You must accomplish this using only standard Bash shell tools.

You have been provided with several artifacts in `/home/user/audit_data/`:

1. `/home/user/audit_data/syslog.log`: A snippet of the system logs.
2. `/home/user/audit_data/shadow.bak`: A backup of a custom credential file containing unsalted MD5 hashes of user passwords in the format `username:md5hash`.
3. `/home/user/audit_data/wordlist.txt`: A dictionary of common passwords.
4. `/home/user/audit_data/passwd.bak`: A backup of the `/etc/passwd` file.
5. `/home/user/audit_data/netstat.txt`: The output of a previously run `netstat -tulpne` command.

Your task is to generate a final audit report by following these steps:

**Phase 1: Log Correlation**
Parse `syslog.log` to identify "compromised" accounts. An account is considered compromised if it has at least 3 "Failed password" attempts from a specific IP address, followed by an "Accepted password" attempt for the same user from the *same* IP address.

**Phase 2: Password Cracking**
For each compromised account identified in Phase 1, extract their password hash from `shadow.bak`. Write a Bash script or one-liner to perform a dictionary attack using `wordlist.txt`. The hashes are unsalted MD5 (equivalent to `echo -n "password" | md5sum | awk '{print $1}'`). Find the plaintext password for each compromised user.

**Phase 3: Service Auditing**
The attackers may have spawned unauthorized listening services under the compromised user accounts. Use `passwd.bak` to map the compromised usernames to their User IDs (UIDs). Then, parse `netstat.txt` to find any TCP ports in the `LISTEN` state owned by those specific UIDs.

**Phase 4: Audit Report Generation**
Correlate all your findings into a single CSV file located at `/home/user/compliance_report.csv`.
The file must have the following header as its first line:
`Username,Attacker_IP,Cracked_Password,Listening_Port`

Append the data for each compromised user you identified.
Ensure the entries are sorted alphabetically by Username.
Do not include users who do not meet all criteria.

*Note: You do not need root access to perform this text analysis. Use built-in Bash commands and coreutils.*