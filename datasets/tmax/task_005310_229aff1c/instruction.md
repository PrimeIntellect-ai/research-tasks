You are a DevSecOps engineer responsible for securing a legacy internal file upload portal. The portal consists of a Python Flask backend and an Nginx reverse proxy. The source code and configuration files are located in `/app/`.

Currently, the system has several security issues:
1. The Flask application (`/app/backend/app.py`) has a path traversal vulnerability (CWE-22) in its file upload handler. Users can upload files to arbitrary locations on the system.
2. The Nginx reverse proxy (`/app/proxy/nginx.conf`) lacks proper security headers and secure cookie configurations.
3. We need a way to automatically detect past intrusion attempts from the Nginx access logs.

Your tasks are:

**1. Fix the Code Vulnerability:**
Audit `/app/backend/app.py` and fix the path traversal vulnerability in the `/upload` endpoint. Ensure that uploaded files are only saved within the `/app/uploads/` directory and cannot escape it, regardless of the filename provided in the request. The backend service runs on port 5000. 

**2. Enforce Security Policy at the Proxy:**
Modify the Nginx configuration at `/app/proxy/nginx.conf`. The proxy listens on port 8080 and forwards to the backend on port 5000. You must add the following security policies:
- Enforce the `Strict-Transport-Security` header (max-age=31536000; includeSubDomains).
- Enforce the `X-Content-Type-Options: nosniff` header.
- Ensure any `Set-Cookie` headers returned by the backend are modified by Nginx to include the `Secure` and `HttpOnly` flags.

**3. Intrusion Detection Script:**
Write a Python script at `/home/user/detect_traversal.py`. This script must read `/app/logs/access.log` (which uses the standard Nginx combined log format) and parse it to find any HTTP requests that attempted a path traversal attack (e.g., payloads containing `../` or `%2e%2e%2f` in the request URI or parameters). 
The script should output the IP addresses of the attackers to `/home/user/compromised_ips.txt`, with one IP address per line, sorted in ascending order, with no duplicates.

**4. Start the Services:**
Once your fixes are applied, start the backend and proxy using the provided startup script: `bash /app/start_services.sh`.

Ensure everything is running smoothly. Our automated verification system will send HTTP requests to port 8080 to verify the upload security, the presence of headers, and the cookie flags.