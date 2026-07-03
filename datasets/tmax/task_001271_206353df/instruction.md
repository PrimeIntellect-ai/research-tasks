You are acting as a security auditor reviewing a compromised web server. 

You have been provided with an SSH authentication log file located at `/home/user/auth.log` and a backup of the web application directory located at `/home/user/webroot`. 

Your objective is to correlate intrusion indicators and audit the web directory for insecure file permissions. 

Please perform the following steps using standard Bash utilities:
1. Parse the `/home/user/auth.log` file to identify the IP address that has the highest number of "Failed password" attempts. 
2. Audit the `/home/user/webroot` directory (and all its subdirectories) to find any files that are world-writable (i.e., write permissions are granted to 'others'). Do not include directories in this list, only files.
3. Generate an audit report located at `/home/user/audit_report.txt` with the following strict format:
   - The first line must contain exactly the single IP address identified in step 1.
   - The subsequent lines must contain the absolute file paths of the world-writable files found in step 2. These paths must be sorted alphabetically.

Ensure your final output file strictly adheres to this structure without any additional text, headers, or blank lines.