You are a DevSecOps engineer performing an incident investigation and policy enforcement. We suspect a poorly designed background job is leaking sensitive credentials via process arguments, and that the executable involved may be improperly configured, posing a privilege escalation risk. 

You have been provided with the following files:
- `/home/user/ps_dump.txt`: A snapshot of process executions.
- `/home/user/wordlist.txt`: A list of common passwords.
- `/home/user/logs/`: A directory containing raw application logs.
- `/home/user/bin/backup_job`: The executable suspected of the leak.

Perform the following tasks using Bash and standard Linux tools:

1. **Investigate the Leak & Crack the Credential:**
   Analyze `/home/user/ps_dump.txt` to find the execution of `/home/user/bin/backup_job`. It takes a command-line argument `--auth-hash` followed by an MD5 hash. Extract this hash and crack it using the provided `/home/user/wordlist.txt`.

2. **Privilege Escalation Audit:**
   Examine the ELF binary `/home/user/bin/backup_job`. Determine if the Set-User-ID (SUID) bit is set. 

3. **Reporting:**
   Create a report file at `/home/user/audit_report.txt` containing exactly one line in the following format:
   `Binary: /home/user/bin/backup_job | SUID: <YES/NO> | Leaked Password: <CRACKED_PLAINTEXT>`
   (Replace `<YES/NO>` with YES if the SUID bit is set, otherwise NO. Replace `<CRACKED_PLAINTEXT>` with the cracked password).

4. **Sensitive Data Redaction:**
   The plaintext password you cracked has unfortunately been logged in plaintext across several files in the `/home/user/logs/` directory. Create a new directory `/home/user/logs_redacted/`. Copy all files from `/home/user/logs/` to `/home/user/logs_redacted/`, replacing every occurrence of the plaintext password with the exact string `[REDACTED]`. Ensure the filenames remain identical.