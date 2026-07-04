You are acting as a compliance analyst tasked with generating an automated security audit trail. You have been provided with application logs and system administration scripts that need to be audited for vulnerabilities. 

Please perform the following steps to complete the audit:

1. **XSS Vulnerability Analysis**: 
   Analyze the web server log file located at `/home/user/logs/access.log`. Identify all IP addresses that have attempted Cross-Site Scripting (XSS) attacks. For this task, an XSS attempt is defined strictly as any HTTP request containing the exact case-sensitive string `<script>`. 
   Extract these IP addresses, sort them in ascending order, ensure they are unique, and write them to `/home/user/xss_ips.txt` (one IP address per line).

2. **Privilege Escalation / Command Injection Auditing**:
   Audit the Python scripts located in the `/home/user/scripts/` directory. One of these scripts contains a critical command injection vulnerability that could lead to privilege escalation (it passes user input from `sys.argv` directly to `os.system()` without sanitization).
   Identify the vulnerable script and write its exact base filename (e.g., `vulnerable.py`) to `/home/user/vuln_script.txt`.

3. **Audit Trail Cryptographic Hashing**:
   To ensure the integrity of your findings for compliance, calculate the SHA-256 cryptographic hash of the `/home/user/xss_ips.txt` file you generated in step 1. Write the resulting hexadecimal digest to `/home/user/audit.sha256` (the file should contain only the hex string, no trailing filenames or spaces). You may write a small Python script to accomplish this or use shell utilities.