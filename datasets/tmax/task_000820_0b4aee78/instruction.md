You are a penetration tester performing a gray-box security assessment and incident response simulation for a local web service. 

An application hosted in `/home/user/vuln_app` has a file upload endpoint that is suspected to be vulnerable to path traversal. Additionally, you need to perform a local privilege escalation audit on the server's configuration backups.

Follow these steps exactly to complete the assessment. Use **Bash** commands and scripts to achieve your objectives.

**Phase 1: TLS/SSL Certificate Management**
The application requires HTTPS to run, but its certificates are missing.
1. Create a directory `/home/user/vuln_app/certs`.
2. Generate a new self-signed RSA 2048-bit certificate and private key valid for 365 days. 
3. Save the certificate as `/home/user/vuln_app/certs/server.crt` and the key as `/home/user/vuln_app/certs/server.key`. The Subject details do not matter.

**Phase 2: Application Startup & Automated Vulnerability Exploitation**
The application code is located at `/home/user/vuln_app/app.py`. It is a Flask application that listens on port 8443 (HTTPS).
1. Install any dependencies found in `/home/user/vuln_app/requirements.txt` using pip.
2. Start the application in the background.
3. The app has an endpoint at `POST /upload` that accepts `multipart/form-data` with a file field named `file`.
4. Exploit the suspected path traversal vulnerability in this endpoint. Craft a `curl` request that uploads a file with the contents "EXPLOIT_SUCCESS". Using the vulnerability, manipulate the filename payload so that the application saves the file exactly to `/home/user/vuln_app/hacked.txt` (the application's base upload directory is `/home/user/vuln_app/uploads`). 

**Phase 3: Security Log Parsing and Correlation**
The application logs upload events to `/home/user/vuln_app/access.log`.
1. After successfully exploiting the endpoint, terminate the background Flask process.
2. Parse the `access.log` file using Bash text processing tools.
3. Find the exact log entry corresponding to your path traversal exploit (the upload containing `../`).
4. Extract ONLY the timestamp string (everything inside the square brackets `[...]`, but do not include the brackets themselves) for that specific exploit request.
5. Save this extracted timestamp string to `/home/user/vuln_app/timestamp.txt`.

**Phase 4: Privilege Escalation Auditing**
You have been provided a backup of the system's sudoers configurations in `/home/user/audit_configs/sudoers.d/`.
1. Scan the files in this directory to identify local privilege escalation vectors.
2. Find the username of the user who has been granted `NOPASSWD` access to execute `/usr/bin/find` as root (a known GTFOBin vector).
3. Write ONLY the exact username of this user to `/home/user/vuln_app/privesc_user.txt`.

Verify your work. Automated tests will evaluate the existence and contents of `server.crt`, `hacked.txt`, `timestamp.txt`, and `privesc_user.txt`.