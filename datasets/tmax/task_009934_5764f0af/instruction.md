You are a forensics analyst investigating a compromised host. You have discovered a local web application that was recently exploited. The application code is located at `/home/user/server.py` and its security configuration is in `/home/user/security.json`.

The application suffers from an open redirect vulnerability in its authentication flow. When a user logs in, the server redirects them to the URL specified in the `next` parameter, insecurely appending the sensitive session token to the query string. The attacker also bypassed the weak Content Security Policy (CSP) defined in `security.json`.

Your task is to analyze the vulnerability, recover the stolen token, and secure the configuration:

1. The vulnerable server relies on Flask. You may need to install it (`pip install flask`) and run the server (`python /home/user/server.py`) in the background to test it. It runs on `http://127.0.0.1:5000`.
2. Write a Python script named `/home/user/exploit.py` that programmatically tests this authentication flow. The script must send a `POST` request to the `/login` endpoint with valid credentials (`username=admin`, `password=admin123`) and a crafted `next` parameter (`http://malicious.local/dump`).
3. Your `exploit.py` script must intercept the HTTP 302 redirect response (do not follow the redirect automatically), extract the exact secret token from the `Location` header, and write *only* the token string to a file at `/home/user/recovered_token.txt`.
4. Enforce Content Security Policy: The application currently loads its headers from `/home/user/security.json`. Modify this JSON file to update the `Content-Security-Policy` value from `default-src *` to strictly `default-src 'self'`.

Ensure your python script executes successfully and generates the `/home/user/recovered_token.txt` file before finishing.