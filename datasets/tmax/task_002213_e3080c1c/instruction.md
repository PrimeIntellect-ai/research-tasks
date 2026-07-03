You are a compliance analyst tasked with generating an audit trail and remediating security vulnerabilities on a mock server environment. You need to process authentication logs for intrusion detection, audit and enforce strict file permissions on SSH private keys, and harden an SSH daemon configuration.

Please perform the following tasks:

1. **Intrusion Detection (Log Analysis)**
   You have been provided with an SSH authentication log file located at `/home/user/auth.log`.
   Write a script (in Python, Perl, Bash, etc.) to analyze this file and identify suspicious IP addresses. An IP address is considered suspicious if it has **more than 3** failed password attempts for the users `root` or `admin`.
   Create a directory `/home/user/audit/` if it does not exist.
   Write the list of suspicious IP addresses to `/home/user/audit/suspicious_ips.log`. The file should contain one IP address per line, sorted in ascending order, with no duplicates.

2. **SSH Key Permission Remediation**
   There is a directory `/home/user/.ssh_mock/` containing various mock SSH keys. 
   Identify all mock private keys (files ending with the `.key` extension). Change the permissions of these private key files to strictly `600` (read and write for the owner only).
   Create a log of your actions by writing the base filenames (not the full path, just the filename, e.g., `id_rsa.key`) of ONLY the files whose permissions you had to change (i.e., files that were not already `600`).
   Write this list to `/home/user/audit/fixed_keys.log`, sorted alphabetically, one filename per line.

3. **SSH Configuration Hardening**
   You will find a mock SSH daemon configuration file at `/home/user/audit_sshd_config`.
   Modify the configuration to meet the following compliance requirements:
   - `PermitRootLogin` must be set to `no`.
   - `PasswordAuthentication` must be set to `no`.
   Leave all other settings exactly as they are. Save the modified configuration file to `/home/user/audit/hardened_sshd_config`.

Ensure all requested output files are placed in `/home/user/audit/` exactly as named.